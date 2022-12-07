import tiledb

def dump_to_db(tile_uri, dataset_uri):
    tiledb.from_csv(
        tile_uri, 
        dataset_uri,
        names=['target','ids','date','flag','user','text'],
        encoding='ISO-8859-1'
        )

if __name__ == "__main__":
    root_dir = "/mnt/data/dataset/twitter/"
    dataset_uri = root_dir + "twitter_sentiment_dataset.csv"
    tile_uri = root_dir + "twitter.tldb"
    
    dump_to_db(tile_uri=tile_uri, dataset_uri=dataset_uri)
