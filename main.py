#Main script for Generating Inventory Report of all the clusters registered under a Prism Central
#Authors: Chinmay Gawde (chinmay.gawde@nutanix.com) and Simran Sunil (simran.sunil@nutanix.com)

import auth, apiCall, pc_inventory, hosts, storage, host_disks, vlans, licensing, replication, vms, ssl_details, snapshots
from openpyxl import Workbook


#Main Function

def getClustersList(pc_name, pcAuthKey):

  url = f"https://{pc_name}:9440/api/nutanix/v3/clusters/list"
  
  clustersData = apiCall.postApiCall(url, pcAuthKey)
  return clustersData
 
if __name__ == "__main__":

    #Get PC name or IP
    pc_name = input("Enter PC Name / PC IP of the cluster to get Configuration: ")
    
    #Get authentication Details
    print("Enter Prism Cental Credentials: ")
    pcAuthKey = auth.auth()
    peAuthKey = ""

    
    wb = Workbook()
    clustersData = getClustersList(pc_name, pcAuthKey)

    print("Select one of the below options:")
    print("1) PC and PE Creds are Same\n2) PC and PE Creds are different but all PE have same Creds\n3) PC and PE Creds are different and all PE have different Creds\n")
    passw = input("Your selection:")
    
    if passw == '2':
        print("Enter Prism Element Credentials: ")
        peAuthKey = auth.auth()

    if passw == '3':
        
        authKeys = {}
        for i in clustersData['entities']:

            if i['status']['resources']['config']['service_list'][0] == "PRISM_CENTRAL":
                continue
            clus_name = i['status']['name']
            print(f"Enter Prism Element Credentials for {clus_name}")
            authKey = auth.auth() 
            authKeys[clus_name] = authKey

            
    if passw == '1':
        peAuthKey = pcAuthKey  


    if clustersData == 0 or clustersData == None:
        print("Exiting")
        
    #Get PC clusters list and sheets
    

    else:

        print(f"Generating all cluster details for Prism Central - {pc_name}")
        if passw == '3':
            pc_inventory.getPCInventory(pc_name,clustersData, pcAuthKey, authKeys, passw, wb)
            hosts.getHostDetails(pc_name,clustersData, pcAuthKey, authKeys, passw, wb)
            vms.getVMsDetails(pc_name,clustersData, pcAuthKey, authKeys, passw, wb)
            storage.getStorageDetails(pc_name,clustersData,pcAuthKey,authKeys,passw,wb)
            host_disks.getHostDiskDetails(pc_name,clustersData,pcAuthKey,authKeys,passw,wb)
            vlans.getvlanDetails(pc_name,clustersData,pcAuthKey,authKeys,passw,wb)
            replication.getReplicationDetails(pc_name,clustersData,pcAuthKey,authKeys,passw,wb)
            snapshots.getsnapshotDetails(pc_name,clustersData,pcAuthKey,authKeys,passw,wb)
            ssl_details.getsslDetails(pc_name,clustersData,pcAuthKey,authKeys,passw,wb)
            licensing.getLicenseDetails(pc_name,clustersData,pcAuthKey,authKeys,passw,wb)
            


        else:
            pc_inventory.getPCInventory(pc_name,clustersData, pcAuthKey, peAuthKey, passw, wb)
            hosts.getHostDetails(pc_name,clustersData, pcAuthKey, peAuthKey, passw, wb)
            vms.getVMsDetails(pc_name,clustersData, pcAuthKey, peAuthKey, passw, wb)
            storage.getStorageDetails(pc_name,clustersData,pcAuthKey,peAuthKey,passw,wb)
            host_disks.getHostDiskDetails(pc_name,clustersData,pcAuthKey,peAuthKey,passw,wb)
            vlans.getvlanDetails(pc_name,clustersData,pcAuthKey,peAuthKey,passw,wb)
            replication.getReplicationDetails(pc_name,clustersData,pcAuthKey,peAuthKey,passw,wb)
            snapshots.getsnapshotDetails(pc_name,clustersData,pcAuthKey,peAuthKey,passw,wb)
            ssl_details.getsslDetails(pc_name,clustersData,pcAuthKey,peAuthKey,passw,wb)
            licensing.getLicenseDetails(pc_name,clustersData,pcAuthKey,peAuthKey,passw,wb)
            
        
        wb.save(f"{pc_name}_Inventory.xlsx")