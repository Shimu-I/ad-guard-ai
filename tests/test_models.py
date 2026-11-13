from decimal import Decimal

import pytest

pytest.importorskip("sqlalchemy")
pytest.importorskip("pydantic_settings")

from sqlalchemy.exc import IntegrityError  # noqa: E402

from app import models  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402
from app.models import (  # noqa: E402
    Ad,
    AdStatus,
    Brand,
    CheckModule,
    CheckResult,
    Product,
    Severity,
    VerificationCheck,
    VerificationReport,
)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def make_ad(db):
    brand = Brand(name="Demo Brand", primary_colors=["#112233"])
    product = Product(brand=brand, name="Demo Tea", price=Decimal("1299.00"), currency="BDT")
    ad = Ad(product=product, headline="Fresh tea", content_hash="aaa")
    db.add_all([brand, product, ad])
    db.commit()
    return brand, product, ad


def test_ad_defaults_and_relationships(db):
    brand, product, ad = make_ad(db)
    assert ad.status == AdStatus.DRAFT
    assert ad.language == "en"
    assert product.brand.name == "Demo Brand"
    assert brand.products == [product]
    assert product.price == Decimal("1299.00")


def test_product_with_ads_cannot_be_hard_deleted(db):
    _, product, _ = make_ad(db)
    db.delete(product)
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_approval_is_invalidated_when_ad_changes(db):
    _, _, ad = make_ad(db)
    ad.status = AdStatus.APPROVED
    ad.approved_content_hash = "aaa"
    assert ad.approval_is_valid
    ad.content_hash = "bbb"  # ad edited after approval
    assert not ad.approval_is_valid


def test_unapproved_ad_has_no_valid_approval(db):
    _, _, ad = make_ad(db)
    assert not ad.approval_is_valid


def test_report_with_no_checks_is_cannot_verify(db):
    _, _, ad = make_ad(db)
    report = VerificationReport(ad=ad, content_hash="aaa")
    assert report.overall_result == CheckResult.CANNOT_VERIFY


def _report_with(db, ad, results):
    report = VerificationReport(ad=ad, content_hash="aaa")
    for i, result in enumerate(results):
        report.checks.append(
            VerificationCheck(
                module=CheckModule.PRICE,
                result=result,
                severity=Severity.CRITICAL if result == CheckResult.ISSUE_FOUND else None,
                message=f"check {i}",
            )
        )
    db.add(report)
    db.commit()
    return report


def test_overall_result_worst_wins(db):
    _, _, ad = make_ad(db)
    assert _report_with(db, ad, [CheckResult.VERIFIED]).overall_result == CheckResult.VERIFIED
    assert (
        _report_with(db, ad, [CheckResult.VERIFIED, CheckResult.CANNOT_VERIFY]).overall_result
        == CheckResult.CANNOT_VERIFY
    )
    assert (
        _report_with(
            db, ad, [CheckResult.VERIFIED, CheckResult.CANNOT_VERIFY, CheckResult.ISSUE_FOUND]
        ).overall_result
        == CheckResult.ISSUE_FOUND
    )


def test_deleting_ad_deletes_its_reports_and_checks(db):
    _, _, ad = make_ad(db)
    _report_with(db, ad, [CheckResult.VERIFIED])
    db.delete(ad)
    db.commit()
    assert db.query(VerificationReport).count() == 0
    assert db.query(VerificationCheck).count() == 0


def test_all_tables_registered():
    names = set(models.Base.metadata.tables)
    assert {"brands", "products", "ads", "verification_reports", "verification_checks"} <= names
