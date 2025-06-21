# sentinel2-downloader

Download sentinel 2 [S2MSI2A](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/product-types/level-2a) data from the [Odata Endpoint](https://documentation.dataspace.copernicus.eu/APIs/OData.html).
Currently only searches the available products and returns the quicklook image links.

## Arguments

The arguments can be given as command line arguments or as a config.yaml

- Point of interest as long,lat SRID=4326 `"POINT(-9.1372 38.7000)"`
- cloudcoverpercentage as float `20`
- datetime range in format `%d-%m-%Y %H:%M:%S,%d-%m-%Y %H:%M:%S`
- maxresults the maximum amount of search results returned.  default=`20`

```shell
Usage: python -m st2dl [OPTIONS] POINTOFINTEREST DATERANGE

  POINTOFINTEREST the point WKT string which is used for the intersect with
  sentinel 2 data. SRID=4326. Example: "POINT(-9.1372 38.7000)"

  DATERANGE the range of dates comma seperated between which is searched. For
  example: "11-08-2023 00:00:00,11-09-2023 00:00:00"

Options:
  -u, --username TEXT         Username for Copernicus Data Space Ecosystem
  -p, --password TEXT
  -m, --max INTEGER           maximum number of results returned  [default:
                              20]
  -c, --cloud-coverage FLOAT  Get only results with a cloud coverage
                              percentage less then the argument given.
                              [default: 25.0]
  --debug                     Debug the http requests and extra debug logging
  --tci                       Download only True Color Image (TCI)
  --help                      Show this message and exit.

```