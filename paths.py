import os

DATA_PATH = "PUT YOUR PATH TO DATA DIR HERE"
URLS_FILE_PATH = os.path.join(DATA_PATH, "url.txt")
SCROBBLES_FILE_PATH = os.path.join(DATA_PATH, "scrobbles.csv")
FESTS_FILE_PATH = os.path.join(DATA_PATH, "fests.json")
MODEL_FILE_PATH = os.path.join(DATA_PATH, "similarities")
FESTS_BACKUP_FILE_PATH = os.path.join(DATA_PATH, "fests_backup.json")
ATENDEES_BACKUP_FILE_PATH = os.path.join(DATA_PATH, "atendees_backup.json")
SCROBBLES_BACKUP_FILE_PATH = os.path.join(DATA_PATH, "scrobbles_backup")
