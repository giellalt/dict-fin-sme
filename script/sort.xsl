<?xml version="1.0" standalone="no"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="r">
  <xsl:for-each select="e">
    <xsl:sort select="lg/l"/>
  </xsl:for-each>
</xsl:template>

</xsl:stylesheet>