<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:template match="/">
		<![CDATA[<!DOCTYPE html>]]>
		<html>
		<head></head>
		<body>
			<xsl:for-each select="history/conversation">
			<div class="conversation">
				<h2><xsl:value-of select="@id"/></h2>
				<xsl:apply-templates select="message"/>
			</div>
			</xsl:for-each>
		</body>
		</html>
	</xsl:template>
	
	<xsl:template match="message">
		<div>
			<strong><xsl:value-of select="author"/></strong>
			<i><xsl:value-of select="timestamp"/></i>
			<p><xsl:value-of select="message"/></p>
		</div>
	</xsl:template>

</xsl:stylesheet>