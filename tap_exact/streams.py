"""Stream type classes for tap-exact."""

from __future__ import annotations

import typing as t

from singer_sdk.typing import (
    StringType,
    IntegerType,
    BooleanType,
    DateTimeType,
    PropertiesList,
    Property,
    NumberType,
)

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


class SalesInvoicesStream(ExactSyncStream):
    """Define SalesInvoices stream."""

    name = "sales_invoices"
    path = "/sync/SalesInvoice/SalesInvoices"
    primary_keys: t.ClassVar[list[str]] = ["ID", "Division"]
    replication_key = "Timestamp"

    schema = PropertiesList(
        Property("Timestamp", IntegerType),
        Property("ID", NumberType),
        Property("Division", IntegerType),
        Property("AmountDC", NumberType),
        Property("AmountDiscount", NumberType),
        Property("AmountDiscountExclVat", NumberType),
        Property("AmountFC", NumberType),
        Property("AmountFCExclVat", NumberType),
        Property("AmountFC", NumberType),
        Property("AmountFCExclVat", NumberType),
        Property("CostCenter", StringType),
        Property("CostCenterDescription", StringType),
        Property("CostUnit", StringType),
        Property("CostUnitDescription", StringType),
        Property("Created", DateTimeType),
        Property("Creator", StringType),
        Property("CreatorFullName", StringType),
        Property("Currency", StringType),
        Property("CustomerItemCode", StringType),
        Property("CustomField", StringType),
        Property("DeliverTo", StringType),
        Property("DeliverToAddress", StringType),
        Property("DeliverToContactPerson", StringType),
        Property("DeliverToContactPersonFullName", StringType),
        Property("DeliverToName", StringType),
        Property("DeliveryDate", DateTimeType),
        Property("Description", StringType),
        Property("Discount", NumberType),
        Property("DiscountType", IntegerType),
        Property("Document", StringType),
        Property("DocumentNumber", StringType),
        Property("DocumentSubject", StringType),
        Property("DueDate", DateTimeType),
        Property("Employee", StringType),
        Property("EmployeeFullName", StringType),
        Property("EndTime", DateTimeType),
        Property("ExtraDutyAmountFC", NumberType),
        Property("ExtraDutyPercentage", NumberType),
        Property("GAccountAmountFC", NumberType),
        Property("GLAccount", StringType),
        Property("GLAccountDescription", StringType),
        Property("ID", StringType),
        Property("IncotermAddress", StringType),
        Property("IncotermCode", StringType),
        Property("IncotermVersion", IntegerType),
        Property("InvoiceDate", DateTimeType),
        Property("InvoiceID", StringType),
        Property("InvoiceNumber", IntegerType),
        Property("InvoiceTo", StringType),
        Property("InvoiceToContactPerson", StringType),
        Property("InvoiceToContactPersonFullName", StringType),
        Property("InvoiceToName", StringType),
        Property("IsExtraDuty", BooleanType),
        Property("Item", StringType),
        Property("ItemCode", StringType),
        Property("ItemDescription", StringType),
        Property("Journal", StringType),
        Property("JournalDescription", StringType),
        Property("LineNumber", IntegerType),
        Property("Modified", DateTimeType),
        Property("Modifier", StringType),
        Property("ModifierFullName", StringType),
        Property("NetPrice", NumberType),
        Property("Notes", StringType),
        Property("OrderDate", DateTimeType),
        Property("OrderedBy", StringType),
        Property("OrderedByContactPerson", StringType),
        Property("OrderedByContactPersonFullName", StringType),
        Property("OrderedByName", StringType),
        Property("OrderNumber", IntegerType),
        Property("PaymentCondition", StringType),
        Property("PaymentConditionDescription", StringType),
        Property("PaymentReference", StringType),
        Property("Pricelist", StringType),
        Property("PricelistDescription", StringType),
        Property("Project", StringType),
        Property("ProjectDescription", StringType),
        Property("ProjectWBS", StringType),
        Property("ProjectWBSDescription", StringType),
        Property("Quantity", NumberType),
        Property("Remarks", StringType),
        Property("SalesChannel", StringType),
        Property("SalesChannelCode", StringType),
        Property("SalesChannelDescription", StringType),
        Property("SalesOrder", StringType),
        Property("SalesOrderLine", StringType),
        Property("SalesOrderLineNumber", IntegerType),
        Property("SalesOrderNumber", IntegerType),
        Property("Salesperson", StringType),
        Property("SalespersonFullName", StringType),
        Property("StarterSalesInvoiceStatus", IntegerType),
        Property("StarterSalesInvoiceStatusDescription", StringType),
        Property("StartTime", DateTimeType),
        Property("Status", IntegerType),
        Property("StatusDescription", StringType),
        Property("Subscription", StringType),
        Property("SubscriptionDescription", StringType),
        Property("TaxSchedule", StringType),
        Property("TaxScheduleCode", StringType),
        Property("TaxScheduleDescription", StringType),
        Property("Timestamp", IntegerType),
        Property("Type", IntegerType),
        Property("TypeDescription", StringType),
        Property("UnitCode", StringType),
        Property("UnitDescription", StringType),
        Property("UnitPrice", NumberType),
        Property("VATAmountDC", NumberType),
        Property("VATAmountFC", NumberType),
        Property("VATCode", StringType),
        Property("VATCodeDescription", StringType),
        Property("VATPercentage", NumberType),
        Property("Warehouse", StringType),
        Property("WithholdingTaxAmountFC", NumberType),
        Property("WithholdingTaxBaseAmount", NumberType),
        Property("WithholdingTaxPercentage", NumberType),
        Property("YourRef", StringType),
    ).to_dict()


class DeletedStream(ExactSyncStream):
    name = "deleted"
    primary_keys = ["ID"]
    path = "/sync/Deleted"
    replication_key = "Timestamp"

    schema = PropertiesList(
        Property("Timestamp", IntegerType),
        Property("DeletedBy", StringType),
        Property("DeletedDate", DateTimeType),
        Property("Division", IntegerType),
        Property("EntityKey", StringType),
        Property("EntityType", IntegerType),
        Property("ID", StringType),
    ).to_dict()


class SalesEntryLinesStream(ExactStream):
    name = "sales_entry_lines"
    primary_keys = ["ID"]
    path = "/salesentry/SalesEntryLines"

    schema = PropertiesList(
        Property("EntryID", StringType),
        Property("AmountDC", NumberType),
        Property("AmountFC", NumberType),
        Property("Asset", StringType),
        Property("AssetDescription", StringType),
        Property("CostCenter", StringType),
        Property("CostCenterDescription", StringType),
        Property("CostUnit", StringType),
        Property("CostUnitDescription", StringType),
        Property("Description", StringType),
        Property("Division", IntegerType),
        Property("ExtraDutyAmountFC", IntegerType),
        Property("ExtraDutyPercentage", NumberType),
        Property("From", StringType),
        Property("GLAccount", StringType),
        Property("GLAccountCode", StringType),
        Property("GLAccountDescription", StringType),
        Property("ID", StringType),
        Property("IntraStatArea", StringType),
        Property("IntraStatCountry", StringType),
        Property("IntraStatDeliveryTerm", StringType),
        Property("IntraStatTransactionA", StringType),
        Property("IntraStatTransactionB", StringType),
        Property("IntraStatTransportMethod", StringType),
        Property("LineNumber", IntegerType),
        Property("Notes", StringType),
        Property("Project", StringType),
        Property("ProjectDescription", StringType),
        Property("Quantity", NumberType),
        Property("SerialNumber", StringType),
        Property("Subscription", StringType),
        Property("StatisticalNumber", StringType),
        Property("StatisticalNetWeight", IntegerType),
        Property("StatisticalValue", IntegerType),
        Property("StatisticalQuantity", IntegerType),
        Property("SubscriptionDescription", StringType),
        Property("TaxSchedule", StringType),
        Property("To", StringType),
        Property("TrackingNumber", StringType),
        Property("TrackingNumberDescription", StringType),
        Property("Type", IntegerType),
        Property("VATAmountDC", NumberType),
        Property("VATAmountFC", NumberType),
        Property("VATBaseAmountDC", NumberType),
        Property("VATBaseAmountFC", NumberType),
        Property("VATCode", StringType),
        Property("VATCodeDescription", StringType),
        Property("CustomField", StringType),
        Property("VATPercentage", NumberType),
    ).to_dict()


class SalesEntriesStream(ExactStream):
    name = "sales_entries"
    primary_keys = ["EntryID"]
    path = "/salesentry/SalesEntries"

    schema = PropertiesList(
        Property("AmountDC", NumberType),
        Property("AmountFC", NumberType),
        Property("BatchNumber", StringType),
        Property("Created", DateTimeType),
        Property("Creator", StringType),
        Property("CreatorFullName", StringType),
        Property("Currency", StringType),
        Property("Customer", StringType),
        Property("CustomerName", StringType),
        Property("Description", StringType),
        Property("Division", IntegerType),
        Property("Document", StringType),
        Property("DocumentNumber", StringType),
        Property("DocumentSubject", StringType),
        Property("DueDate", DateTimeType),
        Property("EntryDate", DateTimeType),
        Property("EntryID", StringType),
        Property("EntryNumber", IntegerType),
        Property("ExternalLinkDescription", StringType),
        Property("ExternalLinkReference", StringType),
        Property("GAccountAmountFC", StringType),
        Property("InvoiceNumber", IntegerType),
        Property("IsExtraDuty", BooleanType),
        Property("Journal", StringType),
        Property("JournalDescription", StringType),
        Property("Modified", DateTimeType),
        Property("Modifier", StringType),
        Property("ModifierFullName", StringType),
        Property("OrderNumber", IntegerType),
        Property("PaymentCondition", StringType),
        Property("PaymentConditionDescription", StringType),
        Property("PaymentConditionPaymentMethod", StringType),
        Property("PaymentReference", StringType),
        Property("ProcessNumber", IntegerType),
        Property("Rate", NumberType),
        Property("ReportingYear", IntegerType),
        Property("ReportingPeriod", IntegerType),
        Property("Reversal", BooleanType),
        Property("Status", IntegerType),
        Property("StatusDescription", StringType),
        Property("Type", IntegerType),
        Property("TypeDescription", StringType),
        Property("VATAmountDC", NumberType),
        Property("VATAmountFC", NumberType),
        Property("WithholdingTaxAmountDC", StringType),
        Property("WithholdingTaxBaseAmount", StringType),
        Property("WithholdingTaxPercentage", StringType),
        Property("YourRef", StringType),
        Property("CustomField", StringType),
        Property("SalesEntryLines", StringType),
    ).to_dict()
