# pysqlsimplecipher
Encrypt or decrypt formated sqlite db.

This project is a tool for sqlite database encryption or decryption like
[sqlcipher](http://sqlcipher.net/)
without install sqlcipher.

When encrypt or decrypt database, an algorithm called AES-256-CBC is used.
Each page shares the same key derived from password,
but owns a random initialization vector stored at the end of the page.

## Decrypt
```bash
python decrypt.py encrypted.db password output.db
```

## Encrypt
```bash
python encrypt.py plain.db password output.db
```
Needs reserved space at the end of each page of the database file.

Otherwise, use sqlcipher to encrypt.

#### Encrypt with sqlcipher
- Open plain db
```bash
./sqlcipher plain.db
```
- Encrypt to enc.db
```sql
ATTACH DATABASE 'enc.db' as encrypted key 'testkey';
SELECT sqlcipher_export('encrypted');
DETACH DATABASE encrypted;
```

## License
GNU Lesser General Public License Version 3
