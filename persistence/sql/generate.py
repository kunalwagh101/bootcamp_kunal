def generate_sql():

    with open("records.sql" ,"w"  ) as f :
        for  i in range(1,501) :
            
            f.write(f"INSERT INTO COMPANIES VALUES ('company{i}', {i});\n")
    print("DONE")



if __name__ == "__main__" :
    generate_sql()