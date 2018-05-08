# Search for SQLite Databases

```
find . \
    -type f \
    -exec \
        file \
        -e apptype \
        -e ascii \
        -e encoding \
        -e tokens \
        -e cdf \
        -e compress \
        -e elf \
        -e tar \
        '{}' \; | \
grep SQLite
```
