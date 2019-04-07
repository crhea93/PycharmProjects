'''
Add an entry to the database
'''

def add_cluster_db(mydb,mycursor,cluster_name,ra,dec,redshift):
    '''
    Add information to cluster table
    :param mydb: my database name
    :param mycursor: cursor name
    :param cluster_name: name of cluster
    :param ra: right ascension in fk5 J2000
    :param dec: declination in fk5 J2000
    :param redshift: redshift of cluster
    :return: none
    '''

    #Check if cluster is already in table
    mycursor.execute(
        "SELECT COUNT(*) FROM Clusters Where Name = %s",
        (cluster_name,)
    )
    (number_of_rows,) = mycursor.fetchone()
    # gets the number of rows affected by the command executed
    mycursor.nextset()
    if number_of_rows == 0:
        # if the cluster doesnt yet exist
        # Lets get the number of clusters current in set
        mycursor.execute("SELECT COUNT(*) FROM Clusters")
        (number_of_rows_curr,) = mycursor.fetchone()
        sql = "INSERT INTO Clusters (ID,Name,ra,decl,redshift) VALUES (%s,%s,%s,%s,%s)"
        val = (number_of_rows_curr,cluster_name, ra, dec, redshift)
        mycursor.execute(sql, val)
        print("Added cluster to database")
    else:
        #Cluster exists
        sql = "UPDATE Clusters SET Name=%s,ra=%s,decl=%s,redshift=%s WHERE Name = %s"
        val = (cluster_name, ra, dec, redshift, cluster_name)
        mycursor.execute(sql, val)
        print("Updated cluster")
    mydb.commit()
    return None

def add_obsid_db(mydb,mycursor,cluster_name,obsid):
    '''
    Add/update obsid for cluster
    :param mydb: my database name
    :param mycursor: my cursor name
    :param cluster_name: name of cluster
    :param obsid: obsid of cluster
    :return: none
    '''
    #Get ID for cluster from Clusters table
    mycursor.execute("SELECT ID FROM Clusters WHERE Name = %s",(cluster_name,))
    (id,) = mycursor.fetchone()
    mycursor.nextset()
    #Check if obsid is already associated with cluster id in obsids table
    mycursor.execute("SELECT COUNT(*) FROM Obsids Where ID = %s",(id,))
    (number_of_rows,) = mycursor.fetchone()
    # gets the number of rows affected by the command executed
    mycursor.nextset()
    if number_of_rows == 0:
        #If the obsid isnt added yet...
        sql = "INSERT INTO Obsids (ID, Obsid) VALUES (%s,%s)"
        vals = (id, obsid)
        mycursor.execute(sql,vals)
        print("Added OBSID to cluster")
    else:
        pass
    mydb.commit()
    return None

def add_fit_db(clust_name,reg_id,area,temp,temp_min,temp_max,abund,ab_min,ab_max,norm,norm_min,norm_max,flux,redchisq):
    '''
    Add fit parameters to database containing regions for each cluster
    :param clust_name: name of cluster
    :param reg_id: id of region (annulus)
    :param area: inner and outer radius of cluster separated by a hyphen
    :param temp: temperature value from fit
    :param temp_min: lower error value for temperature
    :param temp_max: upper error value for temperature
    :param abund: metal abundance value from fit
    :param ab_min: lower error value for metal abundance
    :param ab_max: upper error value for metal abundance
    :param norm: normalization parameter from fit
    :param norm_min: lower error value for normalization
    :param norm_max: upper error value for normalization
    :param flux: flux value from fit
    :param redchisq: reduced chi square value from fit
    '''
    #Get ID for cluster from Clusters table
    mycursor.execute("SELECT ID FROM Clusters WHERE Name = %s",(clust_name,))
    (id,) = mycursor.fetchone()
    mycursor.nextset()
    #Check if obsid is already associated with cluster id in obsids table
    mycursor.execute("SELECT COUNT(*) FROM Region Where idCluster = %s AND idRegion = %s",(id,reg_id))
    (number_of_rows,) = mycursor.fetchone()
    # gets the number of rows affected by the command executed
    mycursor.nextset()
    if number_of_rows == 0:
        # if the cluster doesnt yet exist
        sql = "INSERT INTO Region (Area,Temp,Temp_min,Temp_max,Abundance,Ab_min,Ab_max,Norm,Norm_min,Norm_max,Flux,ReducedChiSquare) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) WHERE idCluster = %s AND idRegion = %s"
        val = (area,temp,temp_min,temp_max,abund,ab_min,ab_max,norm,norm_min,norm_max,flux,redchisq,id,reg_id)
        mycursor.execute(sql, val)
    else:
        #Cluster exists
        sql = "UPDATE Clusters SET Area=%s,Temp=%s,Temp_min=%s,Temp_max=%s,Abundance=%s,Ab_min=%s,Ab_max=%s,Norm=%s,Norm_min=%s,Norm_max=%s,Flux=%s,ReducedChiSquare=%s WHERE idCluster = %s AND idRegion = %s"
        val = (area,temp,temp_min,temp_max,abund,ab_min,ab_max,norm,norm_min,norm_max,flux,redchisq,id,reg_id)
        mycursor.execute(sql, val)
        print("Updated cluster")
    mydb.commit()
    return None
