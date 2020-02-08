import sqlite3
import constants as k

if __name__ == "__main__":
    dna_core = sqlite3.connect(k.dbfile)
    db = dna_core.cursor()

    dna_core.commit()
    db.close()