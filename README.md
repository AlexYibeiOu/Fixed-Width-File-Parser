# Fixed-Width-File-Parser

## User instructions

###Step 1:  Pull the image and start running the container

```dockerfile
docker run -it --name python3.8_fwf ouyibei/fixed_width_file_parser bash
```

###Step 2: Generate fixed-width-file 
```shell
python3 Generate_FWF.py -i spec.json -n 1000000
```

python3   Generate_FWF.py   -i   [spec_file]   -n   [number_of_records]

###Step 3: Parse to CSV file

Copy the generated fixed-width-file name from the output information.

Run below command to parse the file.

```shell
python3 Parse_FWF.py -s spec.json -f [FWF_file_anem]
```

python3   Parse_FWF.py   -s   [spec_file]   -f    [FWF_file_anem]

###Step 4: Check the generated CSV file

```sh
ls ../data/ -lt
```

###Step 5: Download the data folder 

Execute below command on local laptop OS command line.

```
docker cp python3.8_fwf:/Fixed-Width-File-Parser/data/ ./
```

### Step 6: Add new spec file 

Execute below command on local laptop OS command line.

```
docker cp [spec_file] python3.8_fwf:/Fixed-Width-File-Parser/data/
```



## Testing

### Functional Testing

1. Record count checking

2. Columns count checking

3. Width of Column checking

   Testing command:

   ```
   python3 Generate_FWF.py -i spec.json -n 10
   ```

   Generator Result:![Screen Shot 2021-12-16 at 16.28.08](https://tva1.sinaimg.cn/large/008i3skNgy1gxfm3ysza2j30yy09240n.jpg)

   ![Screen Shot 2021-12-16 at 16.29.20](https://tva1.sinaimg.cn/large/008i3skNgy1gxfm46f764j31b60h278q.jpg)

    

   Testing command:

   ```
   python3 Parse_FWF.py -s spec.json -f spec.2021-12-16.16.27.44.694205.FWF
   ```

   Parser Result![Screen Shot 2021-12-16 at 16.34.09](https://tva1.sinaimg.cn/large/008i3skNgy1gxfm88v7hpj31bm0b6n0c.jpg)![Screen Shot 2021-12-16 at 16.35.05](https://tva1.sinaimg.cn/large/008i3skNgy1gxfm8eiui6j31hw0g243f.jpg)

4. File creation checking

   **All results are expected.**

###Failure Scenarios

There are 4 test spec file in /data folder. They cover below 4 failur scenarios. 

1. test1_spec.json

   9 columns with 10 offset value.  

   Test command:

   ```
   python3 Generate_FWF.py -i test1_spec.json -n 10
   ```

   Result:

2. test2_spec.json

   10 columns with 9 offset value.

   Test command:![Screen Shot 2021-12-16 at 16.42.44](https://tva1.sinaimg.cn/large/008i3skNgy1gxfmmpexj0j30yk054t9r.jpg)

   ```
   python3 Generate_FWF.py -i test2_spec.json -n 10
   ```

   Result:![Screen Shot 2021-12-16 at 16.43.41](https://tva1.sinaimg.cn/large/008i3skNgy1gxfmml747qj30ya05475c.jpg)

3. test3_spec.json

   9 columns in spec file, 10 columns in fixed-width-file.

   Expectation: all records rejected.

   Test command:

   ```
   python3 Parse_FWF.py -s test3_spec.json -f spec.2021-12-16.16.27.44.694205.FWF
   ```

   Result:![Screen Shot 2021-12-16 at 16.45.26](https://tva1.sinaimg.cn/large/008i3skNgy1gxfmmbvhzqj313g0bs416.jpg)![Screen Shot 2021-12-16 at 16.46.08](https://tva1.sinaimg.cn/large/008i3skNgy1gxfmlygihyj31ge0i6td8.jpg)

4. test4_spec.json

   11 columns in spec file, 10 columns in fixed-width-file.

   Expectation: all records rejected.

   Test command: 

   ```
   python3 Parse_FWF.py -s test4_spec.json -f spec.2021-12-16.16.47.00.675666.FWF
   ```

   Result:![Screen Shot 2021-12-16 at 16.47.31](https://tva1.sinaimg.cn/large/008i3skNgy1gxfmlm72ixj314c0bwn00.jpg)

   ![Screen Shot 2021-12-16 at 16.47.50](https://tva1.sinaimg.cn/large/008i3skNgy1gxfmleejhtj31ha0ocq8y.jpg)

### More testing

If time allowed, there should be more testing like:

1. Wrong command parameter.
2. Wrong encoding error.
3. Performance testing.
