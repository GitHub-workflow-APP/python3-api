# Python 3 API documentation and test cases

Tickets:

* [RES-2600](https://jira.veracode.local/jira/browse/RES-2600)
	* [BBRD-1654](https://jira.veracode.local/jira/browse/BBRD-1654)
	* [STATIC-19586](https://jira.veracode.local/jira/browse/STATIC-19586)

Master repo: https://gitlab.laputa.veracode.io/research-roadmap/python3-api

[Research Specification](ResearchSpecification.rst)

## Branch RES-2600

https://gitlab.laputa.veracode.io/research-roadmap/python3-api/tree/res-2600

**Scope**: initial API support for Python 3.x

The Simple Scanner can already parse a Py3 application, but doesn't have awareness of the py3 model, so there will be quality issues. This work will specify the Py3 API so that the Simple Scanner can better model it

Due to the size of the included Py3 stdlib, work may need to occur incrementally to support the whole stdlib