# CS744-Project

[Project Proposal](https://drive.google.com/drive/u/2/folders/17alBOquTtHBdmi9bu8b_zSJWVMvB24WF)

### Datasets
1. [Twitter Dataset](https://www.kaggle.com/datasets/kazanova/sentiment140)
2. [ImageNet Dataset](https://image-net.org/download-images.php)

### Installation

#### RocksDB
0. `sudo su`
1. `cd ~`
2. `git clone https://github.com/facebook/rocksdb.git`
3. `cd rocksdb`
4. `DEBUG_LEVEL=0 make shared_lib install-shared`
5. `export LD_LIBRARY_PATH=/usr/local/lib`


### File Structure
- Twitter dataset: /mnt/data/twitter/
