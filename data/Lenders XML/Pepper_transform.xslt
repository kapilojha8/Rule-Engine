<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- Output as HTML -->
  <xsl:output method="html" indent="yes"/>

  <!-- Root template to start the transformation -->
  <xsl:template match="/root">
    <html>
      <head>
        <title>Asset Loan Rules</title>
      </head>
      <body>
        <h1>Asset Loan Rules</h1>
        <xsl:apply-templates select="Lenders/Flexi_up_to_20K/*"/>
      </body>
    </html>
  </xsl:template>

  <!-- Template for each rule-based section (Asset_Type, ABN_Registration, etc.) -->
  <xsl:template match="*">
    <h2><xsl:value-of select="name()"/></h2>
    <table border="1" cellpadding="5">
      <tr>
        <th>Reference Field</th>
        <th>Rule Operator</th>
        <th>Rule Value</th>
        <th>Field Type</th>
      </tr>
      <xsl:apply-templates select="Rule"/>
    </table>
    <xsl:apply-templates select="*"/>
  </xsl:template>

  <!-- Template for the Rule element -->
  <xsl:template match="Rule">
    <tr>
      <td><xsl:value-of select="@Reference_field"/></td>
      <td><xsl:value-of select="@Rule_Operator"/></td>
      <td><xsl:value-of select="@Rule_Value"/></td>
      <td><xsl:value-of select="@Field_Type"/></td>
    </tr>
    <xsl:apply-templates select="Flow_Exception_for_True | Flow_Exception_for_False"/>
  </xsl:template>

  <!-- Template for Flow_Exception elements -->
  <xsl:template match="Flow_Exception_for_True | Flow_Exception_for_False">
    <tr>
      <td colspan="4">
        <b>Flow Exception (Condition: <xsl:value-of select="@Condition_to_proceed"/>):</b>
        <xsl:value-of select="@Remark"/>
      </td>
    </tr>
    <xsl:apply-templates select="Exception_rule/Rule"/>
  </xsl:template>

</xsl:stylesheet>
