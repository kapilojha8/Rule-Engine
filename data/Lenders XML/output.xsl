<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- Root template -->
  <xsl:template match="/">
    <html>
      <head>
        <title>Lender Plans</title>
        <style>
          table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
            padding: 5px;
          }
          th {
            background-color: #f2f2f2;
          }
        </style>
      </head>
      <body>
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
        <h2>Lenders and Their Plans</h2>
        <table>
          <tr>
            <th>Lender Name</th>
            <th>Plan Name</th>
            <th>Rule Name</th>
            <th>Reference Field</th>
            <th>Rule Operator</th>
            <th>Rule Value</th>
            <th>True Evaluation Remark</th>
            <th>False Evaluation Remark</th>
          </tr>
          
          <!-- Loop over Lenders -->
          <xsl:for-each select="root/Lenders/Lender">
            <!-- Loop over Plans -->
            <xsl:for-each select="Plan">
              <!-- Loop over Rules -->
              <xsl:for-each select="Rule">
                <tr>
                  <!-- Lender Name -->
                  <td><xsl:value-of select="../../@name"/></td>
                  <!-- Plan Name -->
                  <td><xsl:value-of select="../@name"/></td>
                  <!-- Rule Name -->
                  <td><xsl:value-of select="@name"/></td>
                  <!-- Reference Field -->
                  <td><xsl:value-of select="@reference_field"/></td>
                  <!-- Rule Operator -->
                  <td><xsl:value-of select="@rule_Operator"/></td>
                  <!-- Rule Value -->
                  <td><xsl:value-of select="@rule_Value"/></td>
                  
                  <!-- Flow for True Evaluation -->
                  <td>
                    <xsl:choose>
                      <xsl:when test="Flow_for_True_eval">
                        <xsl:value-of select="Flow_for_True_eval/@Remark"/>
                      </xsl:when>
                      <xsl:otherwise>N/A</xsl:otherwise>
                    </xsl:choose>
                  </td>
                  
                  <!-- Flow for False Evaluation -->
                  <td>
                    <xsl:choose>
                      <xsl:when test="Flow_for_False_eval">
                        <xsl:value-of select="Flow_for_False_eval/@Remark"/>
                      </xsl:when>
                      <xsl:otherwise>N/A</xsl:otherwise>
                    </xsl:choose>
                  </td>
                </tr>
              </xsl:for-each>
            </xsl:for-each>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
