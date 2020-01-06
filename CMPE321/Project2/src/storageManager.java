import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.TreeMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class storageManager {
	public static final String sc="sc.txt";
	public static final int scRecordSize=35;
	public static final int pageSize=1024;
	public static final int recordHeaderSize=5;
	public static final int pageHeaderSize=9;
	public static final int fileHeaderSize=8;
	
	
	public static void main(String[] args) throws IOException,FileNotFoundException{
		TreeMap<String,Integer> typesActiveFileNumbers=new TreeMap<String,Integer>();
		File inputFile=new File(args[0]);
		File outputFile=new File(args[1]);
        outputFile.createNewFile();
		Scanner input=new Scanner(inputFile);
        BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile,true));
		File systemCatalogue=new File(sc);
		boolean exists = systemCatalogue.exists();
		System.out.println(exists);
		RandomAccessFile sysCat=new RandomAccessFile(sc,"rw");
		sysCat.seek(0);
		if(exists==false) {
			sysCat.writeInt(0);
		}
		else {
		int numOfFile=sysCat.readInt();
		for(int i=0;i<numOfFile;i++) {
			sysCat.seek(4+i*scRecordSize);
			boolean isActive_sc=sysCat.readBoolean();
			String sc_fileName=sysCat.readUTF();
			for(int j=0;j<16-sc_fileName.length();j++) {
				sysCat.readByte();
			}
			String sc_typeName=sysCat.readUTF();
			for(int j=0;j<10-sc_typeName.length();j++) {
				sysCat.readByte();
			}
			int sc_numOfFields=sysCat.readInt();
			if(isActive_sc==true) {
				if(sc_fileName.equals(sc_typeName+"1.txt")) {
					typesActiveFileNumbers.put(sc_typeName, 1);
				}
				else {
					typesActiveFileNumbers.put(sc_typeName, typesActiveFileNumbers.get(sc_typeName)+1);
				}
			}
		}
		}
		while(input.hasNextLine()) {
			String currentLine=input.nextLine();
			String pattern="(\\w)+";
			Pattern p=Pattern.compile(pattern);
			Matcher matcher=p.matcher(currentLine);
			
			List<String> listMatches = new ArrayList<String>();

	        while(matcher.find())
	        {
	            listMatches.add(matcher.group(0));
	        }
	        
	        if(listMatches.size()<2) {
	        	System.out.println("Illegal command");
	        	continue;
	        }
	        String lineRead="";
	        for(int num=0;num<listMatches.size();num++) {
	        	lineRead=lineRead+listMatches.get(num)+" ";
	        }
	        System.out.println(lineRead);
	        String operationPart=listMatches.get(0)+" "+listMatches.get(1);
			if(operationPart.toLowerCase().equals("create type")) {
				ddlCreateType(sysCat,listMatches,typesActiveFileNumbers);
			}
			else if(operationPart.toLowerCase().equals("delete type")) {
				ddlDeleteType(sysCat,listMatches,typesActiveFileNumbers);
			}				
			else if(operationPart.toLowerCase().equals("list type")) {
				ArrayList<String> newOutput=ddlListType(sysCat,listMatches,typesActiveFileNumbers);
				if(newOutput==null) {
					System.out.println("No Types Found!");
					continue;
				}
				if(newOutput != null) {
	                for(String str : newOutput) {
	                    writer.append(str);
	                    writer.newLine();
	                }
	            }
			}
			else if(operationPart.toLowerCase().equals("create record")) {
				dmlCreateRecord(sysCat,listMatches,typesActiveFileNumbers);
			}
			else if(operationPart.toLowerCase().equals("delete record")) {
				dmlDeleteRecord(sysCat,listMatches,typesActiveFileNumbers);
			}
			else if(operationPart.toLowerCase().equals("update record")) {
				dmlUpdateRecord(sysCat,listMatches,typesActiveFileNumbers);
			}
			else if(operationPart.toLowerCase().equals("search record")) {
				dmlSearchRecord(sysCat,listMatches,typesActiveFileNumbers,writer);
			}
			else if(operationPart.toLowerCase().equals("list record")) {
				dmlListRecord(sysCat,listMatches,typesActiveFileNumbers,writer);
			}
			else {
				System.out.println("Illegal Command Entered!");
				continue;
			}
		}
		input.close();
		writer.close();	
		sysCat.close();
	}

	public static void ddlCreateType(RandomAccessFile sc, List<String> inputLine,TreeMap<String,Integer> map) throws FileNotFoundException {
		// TODO Auto-generated method stub
		try {
	        int numOfFields=Integer.parseInt(inputLine.get(3));
	    }
	    catch(Exception e) {
	    	System.out.println("The create type command is not valid!");
	        return;
	    }
		
		int numOfFields=Integer.parseInt(inputLine.get(3));
		if(inputLine.size() != numOfFields + 4) {
			System.out.println("The create type command is not valid!");
			return;
		}
		String typeName=inputLine.get(2);
		String fileName="";
		boolean isTypeFound=false;
		try {
			sc.seek(0);
			int numOfFile=sc.readInt();
			sc.seek(4);
			for(int i=0;i<numOfFile;i++) {
				sc.seek(4+i*scRecordSize);
				boolean isActive_sc=sc.readBoolean();
				String sc_fileName=sc.readUTF();
				for(int j=0;j<16-sc_fileName.length();j++) {
					sc.readByte();
				}
				String sc_typeName=sc.readUTF();
				for(int j=0;j<10-sc_typeName.length();j++) {
					sc.readByte();
				}
				int sc_numOfFields=sc.readInt();
				if(sc_typeName.equals(typeName) && isActive_sc==true) {
					isTypeFound=true;
					System.out.println("The type is already created!");
					sc.seek(0);
					break;
				}
			}
			if(isTypeFound==false) {
				sc.seek(4+numOfFile*scRecordSize);
				fileName=typeName+"1.txt";
				sc.writeBoolean(true);
				sc.writeUTF(fileName);
				for(int i=0;i<16-fileName.length();i++) {
					sc.writeByte(16);
				}
				sc.writeUTF(typeName);
				for(int i=0;i<10-typeName.length();i++) {
					sc.writeByte(10);
				}
				sc.writeInt(numOfFields);
				sc.seek(0); //UPDATE SYS CAT HEADER
				sc.writeInt(numOfFile+1);
				map.put(typeName, 1); //UPDATE MAP
			}
			sc.seek(0);
			try {
				RandomAccessFile newFile=new RandomAccessFile(fileName,"rw");
				newFile.seek(0);
				newFile.writeInt(0);
				newFile.writeInt(0);
				newFile.seek(0);
				newFile.close();
			}
			catch(IOException e){
				System.out.println("Error Code: 102");
			}
		}
		catch(IOException e) {
			System.out.println("Error Code: 101");
			e.getStackTrace();
		}
	}
	
	public static void ddlDeleteType(RandomAccessFile sc,List<String> inputLine,
			TreeMap<String,Integer> map) throws IOException{
		try {
			sc.seek(0);
			int numOfFiles=sc.readInt();
			if(numOfFiles==0 || inputLine.size()!=3) {
				System.out.println("The delete type command is not available!");
				return;
			}
			String typeName=inputLine.get(2);
			boolean isTypeFound=false;
			int count=0;
			int numOfFields=0;
			ArrayList<String> filesToDelete=new ArrayList<String>();
			for(int index=0;index<numOfFiles;index++) {
				sc.seek(4+index*scRecordSize);
				boolean isActive_sc=sc.readBoolean();
				String sc_fileName=sc.readUTF();
				for(int j=0;j<16-sc_fileName.length();j++) {
					sc.readByte();
				}
				String sc_typeName=sc.readUTF();
				for(int j=0;j<10-sc_typeName.length();j++) {
					sc.readByte();
				}
				int sc_numOfFields=sc.readInt();
				if(sc_typeName.equals(typeName) && isActive_sc==true) {
					isTypeFound=true;
					RandomAccessFile file=new RandomAccessFile(sc_fileName,"rw");
					file.seek(0);
					file.setLength(0);
					file.close();
					File f=new File(sc_fileName);
					f.delete();
					sc.seek(4+index*scRecordSize); //Back to SC to set isActive of file -> false
					sc.writeBoolean(false);
				}
			}

			if(isTypeFound==true) {
				map.put(typeName, 0);
			}
			else {
				System.out.println("No such type found!");
			}	

		}
		catch(IOException e) {
			System.out.println("Error Code: 201");
			e.getStackTrace();
		}

	}
	
	public static ArrayList<String> ddlListType(RandomAccessFile sc,List<String> inputLine,TreeMap<String,Integer> map) throws IOException{
		ArrayList<String> typeList=new ArrayList<String>();
		for(Map.Entry<String,Integer> entry : map.entrySet()) {
			  String key = entry.getKey();
			  Integer value = entry.getValue();
			  if(value!=0) {
				  typeList.add(key);
			  }
			}
		Collections.sort(typeList);
		return typeList;
	}
	
	public static void dmlCreateRecord(RandomAccessFile sc,List<String> inputFile,TreeMap<String,Integer> map) throws IOException{
		try {
			boolean isTypeCreated=false;
			boolean isInserted=false;
			String typeName=inputFile.get(2);
			sc.seek(0);
			int numOfFiles=sc.readInt();
			int numOfFields=0;
			for(int i=0;i<numOfFiles;i++) {
				sc.seek(4+i*scRecordSize);
				boolean isActive_sc=sc.readBoolean();
				String sc_fileName=sc.readUTF();
				for(int j=0;j<16-sc_fileName.length();j++) {
					sc.readByte();
				}
				String sc_typeName=sc.readUTF();
				for(int j=0;j<10-sc_typeName.length();j++) {
					sc.readByte();
				}
				if(sc_typeName.equals(typeName) && isActive_sc==true) {
					numOfFields=sc.readInt();
					isTypeCreated=true;
					break;
				}
			}
			if(isTypeCreated==false) {
				System.out.println("Insertion of records before the creation of the type is not allowed!");
				return;
			}
			if(inputFile.size()!=numOfFields+3)return;		
			for(int i=0;i<numOfFiles;i++) { //Scan SysCat
				sc.seek(4+i*scRecordSize);
				boolean isActive_syscat=sc.readBoolean();
				String sc_fileName=sc.readUTF();
				for(int j=0;j<16-sc_fileName.length();j++) {
					sc.readByte();
				}
				String sc_typeName=sc.readUTF();
				for(int j=0;j<10-sc_typeName.length();j++) {
					sc.readByte();
				}
				if(sc_typeName.equals(typeName) && isActive_syscat==true) { //Type is found in a file
					try {
						//int byteSizeRecord=numOfFields*4;
						RandomAccessFile file=new RandomAccessFile(sc_fileName,"rw");
						file.seek(0);
						int numOfTotalPages=file.readInt();
						int numOfActivePages=file.readInt();
						
						for(int m=0;m<numOfTotalPages;m++) {
							file.seek(fileHeaderSize+m*pageSize);//PageHeader
							boolean isActivePage=file.readBoolean();
							int numOfTotalRecords=file.readInt();
							int numOfActiveRecords=file.readInt(); //17 now
							if(isActivePage==true) {
								int recordTotalSize=recordHeaderSize+(numOfFields*4);
								for(int recordScanner=0;recordScanner<numOfTotalRecords;recordScanner++) {
									file.seek((fileHeaderSize+m*pageSize)+pageHeaderSize+(recordScanner*recordTotalSize));
									boolean isActiveRecord=file.readBoolean();
									int numOfFieldsRecord=file.readInt();
									if(isActiveRecord==false) {
										isInserted=true;
										for(int index=0;index<numOfFieldsRecord;index++) {
											file.writeInt(Integer.parseInt(inputFile.get(3+index)));
										}
										//UPDATE RECORD HEADER
										file.seek((fileHeaderSize+m*pageSize)+pageHeaderSize+(recordScanner*recordTotalSize)); //RECORD HEADER
										file.writeBoolean(true);
										//UPDATE PAGE HEADER 
										file.seek((fileHeaderSize+m*pageSize)); //PAGE HEADER
										file.readBoolean();
										file.readInt();
										file.writeInt(numOfActiveRecords+1);
										System.out.println("Record succesfully inserted 1");
										return;
									}
								}
								if(isInserted==false) {
									//TRY TO INSERT IN THE END OF THE ACTIVE PAGE (ALL RECORDS WITHIN THE PAGE IS CURRENTLY ACTIVE)
									if(recordTotalSize*(numOfTotalRecords+1)+pageHeaderSize<=1024) {
										isInserted=true;
										file.seek((fileHeaderSize+m*pageSize)+pageHeaderSize+(numOfTotalRecords*recordTotalSize));
										file.writeBoolean(true);
										file.writeInt(numOfFields);
										for(int index=0;index<numOfFields;index++) {
											file.writeInt(Integer.parseInt(inputFile.get(3+index)));
										}
										//UPDATE PAGE HEADER
										file.seek((fileHeaderSize+m*pageSize)); //PAGE HEADER
										file.readBoolean();
										file.writeInt(numOfTotalRecords+1);
										file.writeInt(numOfActiveRecords+1);
										return;
									}		
								}
							}	
						}
						if(isInserted==false) { //SEARCH THE DELETED PAGES INSIDE THE FILE
							for(int m=0;m<numOfTotalPages;m++) {
								file.seek(fileHeaderSize+m*pageSize);//PageHeader
								boolean isActivePage=file.readBoolean();
								int numOfTotalRecords=file.readInt();
								int numOfActiveRecords=file.readInt(); //17 now
								if(isActivePage==false) {
									isInserted=true;
									file.writeBoolean(true);
									file.readInt();
									for(int index=0;index<numOfFields;index++) {
										file.writeInt(Integer.parseInt(inputFile.get(3+index)));
									}
									//UPDATE PAGE HEADER (Page will become active)
									file.seek(fileHeaderSize+m*pageSize);
									file.writeBoolean(true);
									file.readInt();
									file.writeInt(1);
									//UPDATE FILE HEADER
									file.seek(0);
									file.readInt();
									file.writeInt(numOfActivePages+1);
									return;
								}
							}
						}
						
						if(isInserted==false && numOfTotalPages<20) { //creation of the new page inside the file
							isInserted=true;
							file.seek(fileHeaderSize+numOfTotalPages*pageSize);
							//UPDATE NEW PAGE HEADER
							file.writeBoolean(true);
							file.writeInt(1);
							file.writeInt(1);
							//UPDATE NEW RECORD
							file.writeBoolean(true);
							file.writeInt(numOfFields);
							for(int index=0;index<numOfFields;index++) {
								file.writeInt(Integer.parseInt(inputFile.get(3+index)));
							}
							//UPDATE FILE HEADER
							file.seek(0);
							file.writeInt(numOfTotalPages+1);
							file.writeInt(numOfActivePages+1);
						}
						
						file.close();
					}
					catch(IOException e) {
						System.out.println("Error Code: 403");
					}
					
				}
				
				if(isInserted==true)return;
				else continue;
			}
			
			if(isInserted==false) { //needs creation of new file first insert into systemCat then create new file (all files are searched)
				sc.seek(0);
				int indexNewRecord=4+numOfFiles*scRecordSize;
				sc.seek(indexNewRecord);
				int numOfOccurences=map.get(typeName);
				int indexNewFile=numOfOccurences+1;
				String newFileName=typeName+""+indexNewFile+".txt";
				sc.writeBoolean(true);
				sc.writeUTF(newFileName);
				for(int i=0;i<16-newFileName.length();i++) {
					sc.writeByte(16);
				}
				sc.writeUTF(typeName);
				for(int i=0;i<10-typeName.length();i++) {
					sc.writeByte(10);
				}
				sc.writeInt(numOfFields);
				map.put(typeName, indexNewFile); //UPDATE MAP
				sc.seek(0);
				sc.writeInt(numOfFiles+1); //UPDATE SYS CAT HEADER
				try {//create new file
					RandomAccessFile file=new RandomAccessFile(newFileName,"rw");
					//UPDATE FILE HEADER
					file.seek(0);
					file.writeInt(1);
					file.writeInt(1);
					//UPDATE PAGE HEADER
					file.writeBoolean(true);
					file.writeInt(1);
					file.writeInt(1);
					//CREATE RECORD
					file.writeBoolean(true);
					file.writeInt(numOfFields);
					for(int a=0;a<numOfFields;a++){
						file.writeInt(Integer.parseInt(inputFile.get(a+3)));
					}
					file.close();
				}
				catch(IOException e) {
					System.out.println("Error Code: 402");
					e.getStackTrace();
				}
			}
			
			sc.close();
		}
		catch(IOException e) {
			System.out.println("Error Code: 401");
			e.getStackTrace();
		}
	}
	
	public static void dmlDeleteRecord(RandomAccessFile sc,List<String> inputFile,TreeMap<String,Integer> map) throws IOException {
		if(inputFile.size()!=4) {
			System.out.println("The delete record command is not valid!");
			return;
		}
		String typeName=inputFile.get(2);
		int primaryKey=Integer.parseInt(inputFile.get(3));
		sc.seek(0);
		int numOfFiles=sc.readInt();
		int numOfFields=0;
		boolean isTypeFound=false;
		boolean isDeleted=false;
		for(int i=0;i<numOfFiles;i++) {
			sc.seek(4+i*scRecordSize);
			boolean isActive_sc=sc.readBoolean();
			String sc_fileName=sc.readUTF();
			for(int j=0;j<16-sc_fileName.length();j++) {
				sc.readByte();
			}
			String sc_typeName=sc.readUTF();
			for(int j=0;j<10-sc_typeName.length();j++) {
				sc.readByte();
			}
			if(sc_typeName.equals(typeName) && isActive_sc==true) {
				isTypeFound=true;
				numOfFields=sc.readInt();
				break;
			}
		}
		if(isTypeFound==false) {
			System.out.println("No such type exists!");
			return;
		}
		
		int numOfFilesOfType=map.get(typeName);
		int recordSize=4*numOfFields+recordHeaderSize;
		for(int i=0;i<numOfFilesOfType;i++) { //Search every page of the files of type
			int currentFileIndex=i+1;
			String fileName=typeName+""+currentFileIndex+".txt";
			RandomAccessFile file=new RandomAccessFile(fileName,"rw");
			file.seek(0);
			int numOfTotalPages=file.readInt();
			int numOfActivePages=file.readInt();
			for(int j=0;j<numOfTotalPages;j++) {
				file.seek(fileHeaderSize+j*pageSize); //Point the Page Header
				boolean isActivePage=file.readBoolean();
				int numOfTotalRecords=file.readInt();
				int numOfActiveRecords=file.readInt();
				if(isActivePage==false)continue;
				//else page is active
				file.seek(fileHeaderSize+(j*pageSize)+pageHeaderSize); //Points the Record Header
				for(int m=0;m<numOfTotalRecords;m++) {
					file.seek(fileHeaderSize+(j*pageSize)+pageHeaderSize+(m*recordSize)); //Points the Headers of Records during the search
					boolean isActiveRecord=file.readBoolean();
					int numOfFieldsRecord=file.readInt();
					int primaryKeyRecord=file.readInt();
					if(isActiveRecord==true && primaryKey==primaryKeyRecord) {
						isDeleted=true;
						//RecordFound
						//UPDATE RECORD HEADER
						file.seek(fileHeaderSize+(j*pageSize)+pageHeaderSize+(m*recordSize));
						file.writeBoolean(false);
						//Update Page Header
						file.seek(fileHeaderSize+j*pageSize);
						file.readBoolean();
						file.readInt();
						file.writeInt(numOfActiveRecords-1);
						if(numOfActiveRecords-1==0) {
							//Update Page Header
							file.seek(fileHeaderSize+j*pageSize);
							file.writeBoolean(false);
							//Update File Header
							file.seek(0);
							file.readInt();
							file.writeInt(numOfActivePages-1);
							if(numOfActivePages-1==0) {
								if(!fileName.equals(typeName+"1.txt")) {
									if(!fileName.equals(typeName+"1.txt")) {
										file.seek(0);
										file.setLength(0); //Make sure that the file is empty before deletion
										File f=new File(fileName);
										f.delete();
										sc.seek(0);
										for(int a=0;a<numOfFiles;a++) {
											sc.seek(4+a*scRecordSize); //Get the record belonging to the file in sys cat
											boolean isActiveinSc=sc.readBoolean();
											String sc_fileName=sc.readUTF();
											if(isActiveinSc==true && sc_fileName.equals(fileName)) { //Record found
												sc.seek(4+a*scRecordSize); 
												sc.writeBoolean(false);
												map.put(typeName, map.get(typeName)-1); //Update map
												break;
											}
											
										}
									}
								}
							}
							
						}
					}
				}
			if(isDeleted==true)
				file.close();
				return;
			
			}
			file.close();
		}
		
		if(isDeleted==false) {
			System.out.println("No such record found!");
		}
	}
	
	public static void dmlSearchRecord(RandomAccessFile sc,List<String> inputFile,TreeMap<String,Integer> map,BufferedWriter writer) throws IOException {
		if(inputFile.size()!=4) {
			System.out.println("The search record command is not valid!");
			return;
		}
		String typeName=inputFile.get(2);
		int primaryKey=Integer.parseInt(inputFile.get(3));
		sc.seek(0);
		int numOfFiles=sc.readInt();
		int numOfFields=0;
		boolean isTypeFound=false;
		boolean isRecordFound=false;
		for(int i=0;i<numOfFiles;i++) {
			sc.seek(4+i*scRecordSize);
			boolean isActive_sc=sc.readBoolean();
			String sc_fileName=sc.readUTF();
			for(int j=0;j<16-sc_fileName.length();j++) {
				sc.readByte();
			}
			String sc_typeName=sc.readUTF();
			for(int j=0;j<10-sc_typeName.length();j++) {
				sc.readByte();
			}
			if(sc_typeName.equals(typeName) && isActive_sc==true) {
				isTypeFound=true;
				numOfFields=sc.readInt();
				break;
			}
		}
		if(isTypeFound==false) {
			System.out.println("No such type exists!");
			return;
		}
		
		int numOfFilesOfType=map.get(typeName);
		int recordSize=4*numOfFields+recordHeaderSize;
		for(int i=0;i<numOfFilesOfType;i++) { //Search every page of the files of type
			int currentFileIndex=i+1;
			String fileName=typeName+""+currentFileIndex+".txt";
			RandomAccessFile file=new RandomAccessFile(fileName,"rw");
			file.seek(0);
			int numOfTotalPages=file.readInt();
			int numOfActivePages=file.readInt();
			for(int j=0;j<numOfTotalPages;j++) {
				file.seek(fileHeaderSize+j*pageSize); //Point the Page Header
				boolean isActivePage=file.readBoolean();
				int numOfTotalRecords=file.readInt();
				int numOfActiveRecords=file.readInt();
				if(isActivePage==false)continue;
				//else page is active
				file.seek(fileHeaderSize+(j*pageSize)+pageHeaderSize); //Points the Record Header
				for(int m=0;m<numOfTotalRecords;m++) {
					file.seek(fileHeaderSize+(j*pageSize)+pageHeaderSize+(m*recordSize)); //Points the Headers of Records during the search
					boolean isActiveRecord=file.readBoolean();
					int numOfFieldsRecord=file.readInt();
					int primaryKeyRecord=file.readInt();
					if(isActiveRecord==true && primaryKey==primaryKeyRecord) {
						isRecordFound=true;
						//RecordFound
						file.seek(fileHeaderSize+(j*pageSize)+pageHeaderSize+(m*recordSize));
						file.readBoolean();
						file.readInt();
						String recordContent="";
						for(int index=0;index<numOfFieldsRecord-1;index++) {
							recordContent=recordContent+file.readInt()+" ";
						}
						recordContent=recordContent+file.readInt();
						writer.append(recordContent);
	                    writer.newLine();		
					}
				}
			if(isRecordFound==true)
				file.close();
				return;
			
			}
			file.close();
		}
		
		if(isRecordFound==false) {
			System.out.println("No such record found!");
		}
	}
	
	public static void dmlUpdateRecord(RandomAccessFile sc,List<String> inputFile,TreeMap<String,Integer> map) throws IOException {
		String typeName=inputFile.get(2);
		int primaryKey=Integer.parseInt(inputFile.get(3));
		sc.seek(0);
		int numOfFiles=sc.readInt();
		int numOfFields=0;
		boolean isTypeFound=false;
		boolean isRecordFound=false;
		for(int i=0;i<numOfFiles;i++) {
			sc.seek(4+i*scRecordSize);
			boolean isActive_sc=sc.readBoolean();
			String sc_fileName=sc.readUTF();
			for(int j=0;j<16-sc_fileName.length();j++) {
				sc.readByte();
			}
			String sc_typeName=sc.readUTF();
			for(int j=0;j<10-sc_typeName.length();j++) {
				sc.readByte();
			}
			if(sc_typeName.equals(typeName) && isActive_sc==true) {
				isTypeFound=true;
				numOfFields=sc.readInt();
				break;
			}
		}
		if(inputFile.size()!=numOfFields+3) {
			System.out.println("The update record command is not valid!");
			return;
		}
		if(isTypeFound==false) {
			System.out.println("No such type exists!");
			return;
		}
		
		int numOfFilesOfType=map.get(typeName);
		int recordSize=4*numOfFields+recordHeaderSize;
		for(int i=0;i<numOfFilesOfType;i++) { //Search every page of the files of type
			int currentFileIndex=i+1;
			String fileName=typeName+""+currentFileIndex+".txt";
			RandomAccessFile file=new RandomAccessFile(fileName,"rw");
			file.seek(0);
			int numOfTotalPages=file.readInt();
			int numOfActivePages=file.readInt();
			for(int j=0;j<numOfTotalPages;j++) {
				file.seek(fileHeaderSize+j*pageSize); //Point the Page Header
				boolean isActivePage=file.readBoolean();
				int numOfTotalRecords=file.readInt();
				int numOfActiveRecords=file.readInt();
				if(isActivePage==false)continue;
				//else page is active
				file.seek(fileHeaderSize+(j*pageSize)+pageHeaderSize); //Points the Record Header
				for(int m=0;m<numOfTotalRecords;m++) {
					file.seek(fileHeaderSize+(j*pageSize)+pageHeaderSize+(m*recordSize)); //Points the Headers of Records during the search
					boolean isActiveRecord=file.readBoolean();
					int numOfFieldsRecord=file.readInt();
					int primaryKeyRecord=file.readInt();
					if(isActiveRecord==true && primaryKey==primaryKeyRecord) {
						isRecordFound=true;
						//RecordFound
						file.seek(fileHeaderSize+(j*pageSize)+pageHeaderSize+(m*recordSize));
						file.readBoolean();
						file.readInt();
						file.readInt();
						for(int index=0;index<numOfFieldsRecord-1;index++) {
							file.writeInt(Integer.parseInt(inputFile.get(4+index)));
						}
					}
				}
			if(isRecordFound==true)
				file.close();
				return;
			}
			file.close();
		}
		
		if(isRecordFound==false) {
			System.out.println("No such record found!");
		}
	}
	
	public static void dmlListRecord(RandomAccessFile sc,List<String> inputFile,TreeMap<String,Integer> map,BufferedWriter writer) throws IOException {
		if(inputFile.size()!=3) {
			System.out.println("Illegal list record command!");
			return;
		}
		String typeName=inputFile.get(2);
		if(!map.containsKey(typeName) || map.get(typeName)==0) {
			System.out.println("No such type exists!");
			return;
		}
		TreeMap<Integer,String> recordsMap=new TreeMap<Integer,String>();
		sc.seek(0);
		int numOfFiles=sc.readInt();
		int numOfFields=0;
		for(int i=0;i<numOfFiles;i++) {
			sc.seek(4+i*scRecordSize);
			boolean isActive_sc=sc.readBoolean();
			String sc_fileName=sc.readUTF();
			for(int j=0;j<16-sc_fileName.length();j++) {
				sc.readByte();
			}
			String sc_typeName=sc.readUTF();
			for(int j=0;j<10-sc_typeName.length();j++) {
				sc.readByte();
			}
			if(sc_typeName.equals(typeName) && isActive_sc==true) {
				numOfFields=sc.readInt();
				break;
			}
		}
		int numOfFilesOfType=map.get(typeName);
		int recordSize=4*numOfFields+recordHeaderSize;
		for(int i=0;i<numOfFilesOfType;i++) { //Search every page of the files of type
			int currentFileIndex=i+1;
			String fileName=typeName+""+currentFileIndex+".txt";
			RandomAccessFile file=new RandomAccessFile(fileName,"rw");
			file.seek(0);
			int numOfTotalPages=file.readInt();
			int numOfActivePages=file.readInt();
			for(int j=0;j<numOfTotalPages;j++) {
				file.seek(fileHeaderSize+j*pageSize); //Point the Page Header
				boolean isActivePage=file.readBoolean();
				int numOfTotalRecords=file.readInt();
				int numOfActiveRecords=file.readInt();
				if(isActivePage==false)continue;
				//else page is active
				file.seek(fileHeaderSize+(j*pageSize)+pageHeaderSize); //Points the Record Header
				for(int m=0;m<numOfTotalRecords;m++) {
					file.seek(fileHeaderSize+(j*pageSize)+pageHeaderSize+(m*recordSize)); //Points the Headers of Records during the search
					boolean isActiveRecord=file.readBoolean();
					int numOfFieldsRecord=file.readInt();
					int primaryKeyRecord=file.readInt();
					if(isActiveRecord==true) {
						//RecordFound
						String recordContent="";
						for(int index=0;index<numOfFieldsRecord-2;index++) {
							recordContent=recordContent+file.readInt()+" ";
						}
						recordContent=recordContent+file.readInt();
						recordsMap.put(primaryKeyRecord, recordContent);
					}
				}
				file.close();
			}		
		}
		for(Map.Entry<Integer,String> entry : recordsMap.entrySet()) {
			  Integer key = entry.getKey();
			  String value = entry.getValue();
			  String out=key+" "+value;
			  writer.append(out);
			  writer.newLine();
		}
	}
}
