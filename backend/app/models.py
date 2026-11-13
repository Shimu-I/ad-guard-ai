"""Database models.

Design rules taken from the project's corner cases:

* Brands and products are archived, never hard-deleted while ads still use them
  (foreign keys use RESTRICT).
* An approval is tied to the exact ad content that was approved. If the ad is
  edited afterwards, the approval stops being valid.
* Every verification check returns one of three results: verified, issue found
  or cannot verify. An empty or partly unverifiable report is never "verified".
"""

import enum
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AdStatus(str, enum.Enum):
    DRAFT = "draft"
    NEEDS_FIX = "needs_fix"
    VERIFIED = "verified"
    APPROVED = "approved"


class CheckModule(str, enum.Enum):
    PRICE = "price"
    OCR = "ocr"
    CLAIMS = "claims"
    BRAND = "brand"
    INTEGRITY = "integrity"
    QUALITY = "quality"


class CheckResult(str, enum.Enum):
    VERIFIED = "verified"
    ISSUE_FOUND = "issue_found"
    CANNOT_VERIFY = "cannot_verify"


class Severity(str, enum.Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    SUGGESTION = "suggestion"


def _enum(enum_cls: type[enum.Enum]) -> Enum:
    """Store enum values (e.g. "needs_fix") as plain strings, portable across databases."""
    return Enum(
        enum_cls,
        native_enum=False,
        length=20,
        values_callable=lambda members: [m.value for m in members],
    )


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    primary_colors: Mapped[list] = mapped_column(JSON, default=list)  # hex codes
    secondary_colors: Mapped[list] = mapped_column(JSON, default=list)
    fonts: Mapped[list] = mapped_column(JSON, default=list)
    logo_path: Mapped[str | None] = mapped_column(String(500))
    tone_notes: Mapped[str | None] = mapped_column(Text)
    is_archived: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    products: Mapped[list["Product"]] = relationship(back_populates="brand")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id", ondelete="RESTRICT"), index=True)
    name: Mapped[str] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text)
    # Price is nullable so an incomplete profile can be saved; generation is blocked later.
    price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    original_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(3), default="BDT")
    unit: Mapped[str | None] = mapped_column(String(50))  # e.g. "500g", "1L"
    specs: Mapped[dict] = mapped_column(JSON, default=dict)
    allowed_claims: Mapped[list] = mapped_column(JSON, default=list)
    image_path: Mapped[str | None] = mapped_column(String(500))
    image_sha256: Mapped[str | None] = mapped_column(String(64))  # original photo fingerprint
    is_archived: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    brand: Mapped[Brand] = relationship(back_populates="products")
    ads: Mapped[list["Ad"]] = relationship(back_populates="product")


class Ad(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"), index=True
    )
    headline: Mapped[str | None] = mapped_column(String(300))
    caption: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(10), default="en")
    template_name: Mapped[str | None] = mapped_column(String(100))
    rendered_image_path: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[AdStatus] = mapped_column(_enum(AdStatus), default=AdStatus.DRAFT)
    # Hash of the ad's text and rendered image; changes whenever the ad is edited.
    content_hash: Mapped[str | None] = mapped_column(String(64))
    approved_content_hash: Mapped[str | None] = mapped_column(String(64))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    product: Mapped[Product] = relationship(back_populates="ads")
    reports: Mapped[list["VerificationReport"]] = relationship(
        back_populates="ad",
        cascade="all, delete-orphan",
        order_by="VerificationReport.id",
    )

    @property
    def approval_is_valid(self) -> bool:
        """True only if the ad is approved and unchanged since that approval."""
        return (
            self.status == AdStatus.APPROVED
            and self.approved_content_hash is not None
            and self.approved_content_hash == self.content_hash
        )


class VerificationReport(Base):
    __tablename__ = "verification_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    ad_id: Mapped[int] = mapped_column(ForeignKey("ads.id", ondelete="CASCADE"), index=True)
    # The ad version this report covers, so stale reports can be recognised.
    content_hash: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    ad: Mapped[Ad] = relationship(back_populates="reports")
    checks: Mapped[list["VerificationCheck"]] = relationship(
        back_populates="report",
        cascade="all, delete-orphan",
        order_by="VerificationCheck.id",
    )

    @property
    def overall_result(self) -> CheckResult:
        """Worst result wins; no checks at all means nothing was verified."""
        results = {check.result for check in self.checks}
        if CheckResult.ISSUE_FOUND in results:
            return CheckResult.ISSUE_FOUND
        if not results or CheckResult.CANNOT_VERIFY in results:
            return CheckResult.CANNOT_VERIFY
        return CheckResult.VERIFIED


class VerificationCheck(Base):
    __tablename__ = "verification_checks"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("verification_reports.id", ondelete="CASCADE"), index=True
    )
    module: Mapped[CheckModule] = mapped_column(_enum(CheckModule))
    result: Mapped[CheckResult] = mapped_column(_enum(CheckResult))
    severity: Mapped[Severity | None] = mapped_column(_enum(Severity))  # empty when verified
    message: Mapped[str] = mapped_column(Text)
    suggestion: Mapped[str | None] = mapped_column(Text)
    evidence: Mapped[dict | None] = mapped_column(JSON)  # e.g. expected vs found values

    report: Mapped[VerificationReport] = relationship(back_populates="checks")
