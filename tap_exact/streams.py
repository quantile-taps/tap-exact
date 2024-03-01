"""Stream type classes for tap-exact."""

from __future__ import annotations

import typing as t

from singer_sdk.typing import StringType, IntegerType, BooleanType, DateTimeType, PropertiesList, Property, NumberType

from tap_exact.client import ExactStream, ExactSyncStream


class TransactionLinesStream(ExactSyncStream):
    """Define TransactionLines stream."""

    name = "transaction_lines"
    path = "/sync/Financial/TransactionLines"
    primary_keys: t.ClassVar[list[str]] = ["ID", "Division"]
    replication_key = "Timestamp"
    schema = PropertiesList(
        Property("Timestamp", IntegerType),
        Property("Account", StringType),
        Property("AccountCode", StringType),
        Property("AccountName", StringType),
        Property("AmountDC", NumberType),
        Property("AmountFC", NumberType),
        Property("AmountVATBaseFC", NumberType),
        Property("AmountVATFC", NumberType),
        Property("Asset", StringType),
        Property("AssetCode", StringType),
        Property("AssetDescription", StringType),
        Property("CostCenter", StringType),
        Property("CostCenterDescription", StringType),
        Property("CostUnit", StringType),
        Property("CostUnitDescription", StringType),
        Property("Created", DateTimeType),
        Property("Creator", StringType),
        Property("CreatorFullName", StringType),
        Property("Currency", StringType),
        Property("CustomField", StringType),
        Property("Date", DateTimeType),
        Property("Description", StringType),
        Property("Division", IntegerType),
        Property("Document", StringType),
        Property("DocumentNumber", IntegerType),
        Property("DocumentSubject", StringType),
        Property("DueDate", DateTimeType),
        Property("EntryID", StringType),
        Property("EntryNumber", IntegerType),
        Property("ExchangeRate", NumberType),
        Property("ExternalLinkDescription", StringType),
        Property("ExternalLinkReference", StringType),
        Property("ExtraDutyAmountFC", NumberType),
        Property("ExtraDutyPercentage", NumberType),
        Property("FinancialPeriod", IntegerType),
        Property("FinancialYear", IntegerType),
        Property("GLAccount", StringType),
        Property("GLAccountCode", StringType),
        Property("GLAccountDescription", StringType),
        Property("ID", StringType),
        Property("InvoiceNumber", IntegerType),
        Property("Item", StringType),
        Property("ItemCode", StringType),
        Property("ItemDescription", StringType),
        Property("JournalCode", StringType),
        Property("JournalDescription", StringType),
        Property("LineNumber", IntegerType),
        Property("LineType", IntegerType),
        Property("Modified", DateTimeType),
        Property("ModifierFullName", StringType),
        Property("Notes", StringType),
        Property("OffsetID", StringType),
        Property("OrderNumber", IntegerType),
        Property("PaymentDiscountAmount", NumberType),
        Property("PaymentReference", StringType),
        Property("Project", StringType),
        Property("ProjectCode", StringType),
        Property("ProjectDescription", StringType),
        Property("Quantity", NumberType),
        Property("SerialNumber", StringType),
        Property("Status", IntegerType),
        Property("Subscription", StringType),
        Property("SubscriptionDescription", StringType),
        Property("TrackingNumber", StringType),
        Property("TrackingNumberDescription", StringType),
        Property("Type", IntegerType),
        Property("VATCode", StringType),
        Property("VATCodeDescription", StringType),
        Property("VATPercentage", NumberType),
        Property("VATType", StringType),
        Property("YourRef", StringType),
    ).to_dict()


class GLAccountsStream(ExactSyncStream):
    """Define GLAccounts stream."""

    name = "gl_accounts"
    path = "/sync/Financial/GLAccounts"
    primary_keys: t.ClassVar[list[str]] = ["ID", "Division"]
    replication_key = "Timestamp"
    schema = PropertiesList(
        Property("Timestamp", IntegerType),
        Property("AllowCostsInSales", BooleanType),
        Property("AssimilatedVATBox", IntegerType),
        Property("BalanceSide", StringType),
        Property("BalanceType", StringType),
        Property("BelcotaxType", IntegerType),
        Property("Code", StringType),
        Property("Compress", BooleanType),
        Property("Costcenter", StringType),
        Property("CostcenterDescription", StringType),
        Property("Costunit", StringType),
        Property("CostunitDescription", StringType),
        Property("Created", DateTimeType),
        Property("Creator", StringType),
        Property("CreatorFullName", StringType),
        Property("CustomField", StringType),
        Property("Description", StringType),
        Property("Division", IntegerType),
        Property("ExcludeVATListing", BooleanType),
        Property("ExpenseNonDeductiblePercentage", NumberType),
        Property("ID", StringType),
        Property("IsBlocked", BooleanType),
        Property("Matching", BooleanType),
        Property("Modified", DateTimeType),
        Property("Modifier", StringType),
        Property("ModifierFullName", StringType),
        Property("PrivateGLAccount", StringType),
        Property("PrivatePercentage", NumberType),
        Property("ReportingCode", BooleanType),
        Property("RevalueCurrency", BooleanType),
        Property("SearchCode", StringType),
        Property("Type", IntegerType),
        Property("TypeDescription", StringType),
        Property("UseCostcenter", BooleanType),
        Property("UseCostunit", BooleanType),
        Property("VATCode", StringType),
        Property("VATDescription", StringType),
        Property("VATGLAccountType", StringType),
        Property("VATNonDeductibleGLAccount", StringType),
        Property("VATNonDeductiblePercentage", NumberType),
        Property("VATSystem", StringType),
        Property("YearEndCostGLAccount", StringType),
        Property("YearEndReflectionGLAccount", StringType),
    ).to_dict()


class GLClassificationsStream(ExactSyncStream):
    """Define GLClassifications stream."""

    name = "gl_classifications"
    path = "/sync/Financial/GLClassifications"
    primary_keys: t.ClassVar[list[str]] = ["ID", "Division"]
    replication_key = "Timestamp"
    schema = PropertiesList(
        Property("Timestamp", IntegerType),
        Property("Abstract", BooleanType),
        Property("Balance", StringType),
        Property("Code", StringType),
        Property("Created", DateTimeType),
        Property("CreatorFullName", StringType),
        Property("Description", StringType),
        Property("Division", IntegerType),
        Property("ID", StringType),
        Property("IsTupleSubElement", BooleanType),
        Property("Modified", DateTimeType),
        Property("Modifier", StringType),
        Property("ModifierFullName", StringType),
        Property("Name", StringType),
        Property("Nillable", BooleanType),
        Property("Parent", StringType),
        Property("PeriodType", StringType),
        Property("SubstitutionGroup", StringType),
        Property("TaxonomyNamespace", StringType),
        Property("TaxonomyNamespaceDescription", StringType),
        Property("Type", StringType),
    ).to_dict()


class GLAccountClassificationMappingsStream(ExactStream):
    """Define GLAccountClassificationMappings stream."""

    name = "gl_account_classification_mappings"
    path = "/Financial/GLAccountClassificationMappings"
    primary_keys: t.ClassVar[list[str]] = ["ID", "Division"]
    schema = PropertiesList(
        Property("ID", StringType),
        Property("Classification", StringType),
        Property("ClassificationCode", StringType),
        Property("ClassificationDescription", StringType),
        Property("Division", IntegerType),
        Property("GLAccount", StringType),
        Property("GLAccountCode", StringType),
        Property("GLAccountDescription", StringType),
        Property("GLSchemeCode", StringType),
        Property("GLSchemeDescription", StringType),
        Property("GLSchemeID", StringType),
    ).to_dict()


class DeletedStream(ExactSyncStream):
    name = "deleted"
    primary_keys = ["ID"]
    path = "/sync/Deleted"
    replication_key = "Timestamp"

    schema = PropertiesList(
        Property("Timestamp", StringType),
        Property("DeletedBy", StringType),
        Property("DeletedDate", DateTimeType),
        Property("Division", StringType),
        Property("EntityKey", StringType),
        Property("EntityType", StringType),
        Property("ID", StringType),
    ).to_dict()