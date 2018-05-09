# Search for Private Keys

```
find / -xdev -type f -print0 | xargs -0 grep -H "BEGIN RSA PRIVATE KEY"
```

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
