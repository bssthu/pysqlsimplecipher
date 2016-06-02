# pysqlsimplecipher
Encrypt or decrypt formated sqlite db.

This project is a tool for sqlite database encryption or decryption like
[sqlcipher](http://sqlcipher.net/)
without install sqlcipher.

## Decrypt
```bash
python decrypt.py encrypted.db password output.db
```

## Encrypt
```bash
python encrypt.py plain.db password output.db
```
Needs reserved space at the end of each page of the database file.

## License
GNU Lesser General Public License Version 3
