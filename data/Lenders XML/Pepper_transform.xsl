<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Output method as HTML -->
    <xsl:output method="html" indent="yes" />

    <!-- Template for the root element -->
    <xsl:template match="/root">
        <html>
            <head>
                <title>Loan Information</title>
                <style>
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h1>Loan Application Information</h1>

                <!-- Field Types -->
                <h2>Field Types</h2>
                <table>
                    <tr>
                        <th>Field Type</th>
                        <th>Value</th>
                    </tr>
                    <xsl:for-each select="Field_type/*">
                        <tr>
                            <td><xsl:value-of select="name()" /></td>
                            <td><xsl:value-of select="." /></td>
                        </tr>
                    </xsl:for-each>
                </table>

                <!-- Remarks -->
                <h2>Remarks</h2>
                <table>
                    <tr>
                        <th>Remark</th>
                    </tr>
                    <xsl:for-each select="Remarks/*">
                        <tr>
                            <td><xsl:value-of select="." /></td>
                        </tr>
                    </xsl:for-each>
                </table>

                <!-- Lenders Information -->
                <h2>Lenders: Flexi up to 20K</h2>
                <table>
                    <tr>
                        <th>Reference Field</th>
                        <th>Rule Operator</th>
                        <th>Field Type</th>
                        <th>Rule Value</th>
                        <th>Flow Exception True</th>
                        <th>Flow Exception False</th>
                    </tr>

                    <!-- Asset_Type -->
                    <tr>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Asset_Type/@Reference_field" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Asset_Type/@Rule_Operator" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Asset_Type/@Field_Type" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Asset_Type/@Rule_Value" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Asset_Type/Flow_Exception_for_True/@Remark" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Asset_Type/Flow_Exception_for_False/@Remark" /></td>
                    </tr>

                    <!-- ABN_Registration -->
                    <tr>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/ABN_Registration/@Reference_field" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/ABN_Registration/@Rule_Operator" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/ABN_Registration/@Field_Type" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/ABN_Registration/@Rule_Value" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/ABN_Registration/Flow_Exception_for_True/@Remark" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/ABN_Registration/Flow_Exception_for_False/@Remark" /></td>
                    </tr>

                    <!-- GST_Registration -->
                    <tr>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/GST_Registration/@Reference_field" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/GST_Registration/@Rule_Operator" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/GST_Registration/@Field_Type" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/GST_Registration/@Rule_Value" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/GST_Registration/Flow_Exception_for_True/@Remark" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/GST_Registration/Flow_Exception_for_False/@Remark" /></td>
                    </tr>

                    <!-- Loan_Amount -->
                    <tr>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Loan_Amount/@Reference_field" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Loan_Amount/@Rule_Operator" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Loan_Amount/@Field_Type" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Loan_Amount/@Rule_Value" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Loan_Amount/Flow_Exception_for_True/@Remark" /></td>
                        <td><xsl:value-of select="Lenders/Flexi_up_to_20K/Loan_Amount/Flow_Exception_for_False/@Remark" /></td>
                    </tr>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
