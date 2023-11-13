# sentinel2-downloader

Download sentinel 2 [S2MSI2A](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/product-types/level-2a) data from the [Odata Endpoint](https://documentation.dataspace.copernicus.eu/APIs/OData.html).
Currently only searches the available products and returns the quicklook image links.

## Arguments

The arguments can be given as command line arguments or as a config.yaml

- Point of interest as long,lat SRID=4326 `"POINT(-9.1372 38.7000)"`
- cloudcoverpercentage as float `20`
- datetime range in format `%d-%m-%Y %H:%M:%S,%d-%m-%Y %H:%M:%S`
- maxresults the maximum amount of search results returned.  default=`20`

