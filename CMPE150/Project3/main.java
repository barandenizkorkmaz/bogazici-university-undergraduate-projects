import java.io.*;	//Enables us to create virtual files.
import java.util.*;	//Enables us to read files and user's entries which allows us to communicate user and computer.

public class main {
    public static void main(String[] args) throws FileNotFoundException{	//throws command prevents a likely error causing due to not-found file.
        Random rand = new Random();	//rand enables computers to make random moves which will be used later.
        Scanner input = new Scanner(new File("input.txt"));	//input enables us to read file.
        Scanner console = new Scanner(System.in);			//console enables player to make moves which will be used later.

        String firstRow = input.nextLine();	//The first row of the input is stored as String in firstRow.
        String secondRow = input.nextLine();//The second row of the input is stored as String in secondRow.
        String thirdRow = input.nextLine();	//The first row of the input is stored as String in thirdRow.
        String fourthRow = input.nextLine();//The first row of the input is stored as String in forthRow.
        String fifthRow = input.nextLine();	//The first row of the input is stored as String in fifthRow.
        String sixthRow = input.nextLine();	//The first row of the input is stored as String in sixthRow.

        String [] row1 = new String[6];	//For each row an array created which will store each row later.
        String [] row2 = new String[6];
        String [] row3 = new String[6];
        String [] row4 = new String[6];
        String [] row5 = new String[6];
        String [] row6 = new String[6];



        for(int i = 0 ; i<6 ; i++){	//This for loop enables us to store each character of the row in each index of arrays.
            row1[i] = "" + firstRow.substring(i,i+1);
            row2[i] = "" + secondRow.substring(i,i+1);
            row3[i] = "" + thirdRow.substring(i,i+1);
            row4[i] = "" + fourthRow.substring(i,i+1);
            row5[i] = "" + fifthRow.substring(i,i+1);
            row6[i] = "" + sixthRow.substring(i,i+1);
        }

        String table = "";	//String table is created so as to store configuration of the board as a single line.

        for(int i = 0 ; i<6 ; i++){	//As defined just above, by this for loops , we are adding each indexes of arrays one by one into a single lined string (String table).
            table += row1[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row2[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row3[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row4[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row5[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row6[i];
        }

        int hand = 0; //int hand implies whose turn is it.

        while(!controller(row1,row2,row3,row4,row5,row6,table)){ //Until boolean controller is false which implies still there's no winner. The program enters into while loop.
            if(hand%2 == 0){	//As mentioned above, if hand%2==0 it's player's turn. This method also enables player to play first.Until one side wins they keep playing one by one.
                System.out.println("Please enter your move: ");
                String playersDecision = console.next();	//Next character will be entered by the user will imply player's next move.
                if(playersDecision.equals("C")){	//If the character entered is C, following steps will be executed.
                    int x1 = console.nextInt();		//Coordinates entered by the user will be stored in int x1 and int y1.
                    int y1 = console.nextInt();
                    while(!changeController(x1,y1,table)){	//While boolean changeController is false it will want user to enter new coordinates which are valid.
                        System.out.println("Please enter valid coordinates: ");
                        playersDecision = console.next();
                        x1 = console.nextInt();
                        y1 = console.nextInt();
                    }
                    table = playersChange(row1,row2,row3,row4,row5,row6,x1,y1); //When the user enters valid coordinates, playerChange method will be executed.
                    for(int j = 0; j<6 ; j++){  //Following for loops will print current board configuration after move is executed succesfully.
                        row1[j%6]=table.substring(j,j+1);
                        System.out.print(row1[j%6]);
                    }
                    System.out.println("");
                    for(int j=6 ; j<12 ; j++){
                        row2[j%6]=table.substring(j,j+1);
                        System.out.print(row2[j%6]);
                    }
                    System.out.println("");
                    for(int j=12 ; j<18; j++){
                        row3[j%6]=table.substring(j,j+1);
                        System.out.print(row3[j%6]);
                    }
                    System.out.println("");
                    for(int j=18 ; j<24; j++){
                        row4[j%6]=table.substring(j,j+1);
                        System.out.print(row4[j%6]);
                    }
                    System.out.println("");
                    for(int j=24 ; j<30; j++){
                        row5[j%6]=table.substring(j,j+1);
                        System.out.print(row5[j%6]);
                    }
                    System.out.println("");
                    for(int j=30 ; j<36; j++){
                        row6[j%6]=table.substring(j,j+1);
                        System.out.print(row6[j%6]);
                    }
                    System.out.println("");

                }
                else if(playersDecision.equals("M")){	//If player enters 'M' which means the player wants to make a move action, the program skips the first option (which is change action)
                    int x1 = console.nextInt();			//By the following integers int x1,y1,x2 and y2 we store coordinate which will be moved and which is target.
                    int y1 = console.nextInt();
                    int x2 = console.nextInt();
                    int y2 = console.nextInt();

                    while(!movePlayerController(x1, y1 ,x2, y2 , table)){	//While movePlayerController is false, the program wants user to enter new valid coordinates.
                        System.out.println("Please enter valid coordinates: ");
                        playersDecision = console.next();
                        x1 = console.nextInt();
                        y1 = console.nextInt();
                        x2 = console.nextInt();
                        y2 = console.nextInt();
                    }
                    table = playersMove(x1,y1,x2,y2,table);	//When the player enters valid coordinates, playersMove method which makes move action will be executed.

                    for(int j = 0; j<6 ; j++){	//Following for loops will print current board configuration after move is executed succesfully.
                        row1[j%6]=table.substring(j,j+1);
                        System.out.print(row1[j%6]);
                    }
                    System.out.println("");
                    for(int j=6 ; j<12 ; j++){
                        row2[j%6]=table.substring(j,j+1);
                        System.out.print(row2[j%6]);
                    }
                    System.out.println("");
                    for(int j=12 ; j<18; j++){
                        row3[j%6]=table.substring(j,j+1);
                        System.out.print(row3[j%6]);
                    }
                    System.out.println("");
                    for(int j=18 ; j<24; j++){
                        row4[j%6]=table.substring(j,j+1);
                        System.out.print(row4[j%6]);
                    }
                    System.out.println("");
                    for(int j=24 ; j<30; j++){
                        row5[j%6]=table.substring(j,j+1);
                        System.out.print(row5[j%6]);
                    }
                    System.out.println("");
                    for(int j=30 ; j<36; j++){
                        row6[j%6]=table.substring(j,j+1);
                        System.out.print(row6[j%6]);
                    }
                    System.out.println("");
                }
            }

            else{	//If hand%2 is not equal to 0 (it is equal to 1 in this case) this implies it's computer's turn and computer will make its move.
                System.out.println("Computer's move:");
                int computersDecision = rand.nextInt(2);	//Computer decides randomly to which move it's going to make.
                if(hand==1 || computersDecision==0){		//If the integer chosen randomly is 0, computer makes a change action. If int hand=1 the computer automatically makes a change action due to lack of "O" which is wanted to be moved.
                    int x1 = rand.nextInt(6);				//Computer randomly selects the coordinates of the point which will be changed to "O".
                    int y1 = rand.nextInt(6);
                    while(!changeController(x1,y1,table)){	//While the coordinates are not valid, the computer keeps selecting new coordinates randomly until the coordinates are valid.
                        x1 = rand.nextInt(6);
                        y1 = rand.nextInt(6);

                    }
                    table = computersChange(row1,row2,row3,row4,row5,row6,x1,y1);  //After the computer randomly selected two coordinates computersChange method will be executed.

                    for(int j = 0; j<6 ; j++){	//Following for loops will print current board configuration after move is executed succesfully.
                        row1[j%6]=table.substring(j,j+1);
                        System.out.print(row1[j%6]);
                    }
                    System.out.println("");
                    for(int j=6 ; j<12 ; j++){
                        row2[j%6]=table.substring(j,j+1);
                        System.out.print(row2[j%6]);
                    }
                    System.out.println("");
                    for(int j=12 ; j<18; j++){
                        row3[j%6]=table.substring(j,j+1);
                        System.out.print(row3[j%6]);
                    }
                    System.out.println("");
                    for(int j=18 ; j<24; j++){
                        row4[j%6]=table.substring(j,j+1);
                        System.out.print(row4[j%6]);
                    }
                    System.out.println("");
                    for(int j=24 ; j<30; j++){
                        row5[j%6]=table.substring(j,j+1);
                        System.out.print(row5[j%6]);
                    }
                    System.out.println("");
                    for(int j=30 ; j<36; j++){
                        row6[j%6]=table.substring(j,j+1);
                        System.out.print(row6[j%6]);
                    }
                    System.out.println("");
                }

                else if (hand!=1 && computersDecision==1){	//If hand is not equal to 1 and computersDecision equals 1, it means that the program randomly decided to make a move action.
                    int x1 = rand.nextInt(6);	//By the following integers int x1,y1,x2 and y2 we store coordinate which will be moved and which is target.
                    int y1 = rand.nextInt(6);
                    int x2 = rand.nextInt(6);
                    int y2 = rand.nextInt(6);
                    while(!moveComputerController(x1, y1 ,x2, y2 , table)){	//While moveComputerController is false, the program wants computer to enter new valid coordinates which will be selected randomly.

                        x1 = rand.nextInt(6);
                        y1 = rand.nextInt(6);
                        x2 = rand.nextInt(6);
                        y2 = rand.nextInt(6);
                    }
                    table = computersMove(x1,y1,x2,y2,table);	//When the computer enters valid coordinates, computersMove method which makes move action will be executed.

                    for(int j = 0; j<6 ; j++){	//Following for loops will print current board configuration after move is executed succesfully.
                        row1[j%6]=table.substring(j,j+1);
                        System.out.print(row1[j%6]);
                    }
                    System.out.println("");
                    for(int j=6 ; j<12 ; j++){
                        row2[j%6]=table.substring(j,j+1);
                        System.out.print(row2[j%6]);
                    }
                    System.out.println("");
                    for(int j=12 ; j<18; j++){
                        row3[j%6]=table.substring(j,j+1);
                        System.out.print(row3[j%6]);
                    }
                    System.out.println("");
                    for(int j=18 ; j<24; j++){
                        row4[j%6]=table.substring(j,j+1);
                        System.out.print(row4[j%6]);
                    }
                    System.out.println("");
                    for(int j=24 ; j<30; j++){
                        row5[j%6]=table.substring(j,j+1);
                        System.out.print(row5[j%6]);
                    }
                    System.out.println("");
                    for(int j=30 ; j<36; j++){
                        row6[j%6]=table.substring(j,j+1);
                        System.out.print(row6[j%6]);
                    }
                    System.out.println("");
                }
            }
            hand++;	//When one's turn ends hand will be increased by one so as to charge other one to make action.
        }
        if(hand%2==1){	//When the program exits while loop which implies controller is true now (which implies there's a winner), if hand%2=1 this means user has won, otherwise the computer has won.
            System.out.println("You have won the game ! ");
        }
        else{
            System.out.println("The computer has won the game ! ");
        }
    }
    /*	playersChange method enables player to make change action. The method takes 6 arrays which are each row of the board as mentioned before
        and 2 integers int x1 and int y1 as parameters which indicates the coordinates of the target point which will be changed to "X".
         By nested if/else if/else structure the program changes blank "B" pieces into "X" considering the target coordinates. Eventually, it returns
         the current configuration of the board as rows stored in strings (row1,row2,row3 and so on) after change action is made succesfully.
     */
    public static String playersChange(String[] row1,String[] row2,String[] row3,String[] row4,String[] row5,String[] row6,int x1, int y1){
        String table = "";
        if(x1==0){
            row1[y1]="X";
        }
        else if(x1==1){
            row2[y1]="X";
        }
        else if(x1==2){
            row3[y1]="X";
        }
        else if(x1==3){
            row4[y1]="X";
        }
        else if(x1==4){
            row5[y1]="X";
        }
        else{
            row6[y1]="X";
        }

        for(int i = 0 ; i<6 ; i++){
            table += row1[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row2[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row3[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row4[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row5[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row6[i];
        }
        return table;
    }
	
	/*	playersChange method enables player to make move action. The method takes String table 
	 	which will be used to return current configuration of the board
	 	mentioned as String copy and 4 integers int x1, int y1, int x2, int y2 as parameters 
	 	which indicates the coordinates of the point which will be moved and the target point 
	 	into where we will the moved point will be replaced.
	 */
	
	/* Move action will be organised by the if and else ifs again.
	   In the move action, 2 possibility exists.
	   Move in the row and move in the column.
	   First the method checks if x1=x2 which implies that the move action is in the row.
	   Then the method checks whether y1<y2 or otherwise.
	   If y1>y2 this implies the target coordinate is at the beginning of the row such as 4 0 (4 5 to 4 0).
	   Otherwise (y1<y2) the target coordinate is in the end of the row such as 4 5 (4 0 to 4 5).
	   And finally new string copy is organised in order to store the new configuration of the board reorganized by substring and charAt methods and is returned.
	   Same system is applied for the case in which y1=y2 in the following part of the method.
	   If y1=y2, this implies that the move action is in the column.
	   If x1<x2 this implies the target coordinate is in the end of the column such as 0 5 (0 0 to 5 0).
	   Otherwise (x1>x2) the target coordinate is at the beginning of the row such as 3 0 (5 3 to 0 3).
	   And finally new string copy is organised in order to store the new configuration of the board reorganized by substring and charAt methods and is returned.
	*/

    public static String playersMove(int x1,int y1,int x2,int y2,String table){
        String copy = table;
        if(x1==x2){
            if(y1<y2){
                copy=table.substring(0,6*x1+y1)+table.substring(6*x1+y1+1,6*x1+y2+1)+table.charAt(6*x1+y1)+table.substring(6*(x1+1));
            }
            else if(y1>y2){
                copy=table.substring(0,6*x1)+table.charAt(6*x1+y1)+table.substring(6*x1,6*x2+y1)+table.substring(6*(x1)+y1+1);
            }
        }
        else if(y1==y2){
            if(x1<x2){
                copy = table.substring(0,6*x1+y1);
                for(int i=1 ; i<=x2-x1; i++){
                    copy +=  table.charAt(6*(x1+i)+y1)+ table.substring(6*x1+y1+1 +6*(i-1),6*(x1+i)+y1);
                }
                copy += table.charAt(6*x1+y1) + table.substring(6*(x2)+y2+1);
            }
            else if(x1>x2){
                copy=table.substring(0,y2)+table.charAt(6*x1+y1);
                for(int i=1;i<=(x1-x2);i++){
                    copy+=table.substring(6*(x2+i-1)+y2+1,6*(x2+i)+y2)+table.charAt(6*(x2+i-1)+y2);
                }
                copy+=table.substring(6*x1+y1+1);
            }
        }
        return copy;
    }

    /*
         computersChange works in the same manner in the method "playersChange".
    */
    public static String computersChange(String[] row1,String[] row2,String[] row3,String[] row4,String[] row5,String[] row6,int x1, int y1){
        String table = "";
        if(x1==0){
            row1[y1]="O";
        }
        else if(x1==1){
            row2[y1]="O";
        }
        else if(x1==2){
            row3[y1]="O";
        }
        else if(x1==3){
            row4[y1]="O";
        }
        else if(x1==4){
            row5[y1]="O";
        }
        else{
            row6[y1]="O";
        }
        for(int i = 0 ; i<6 ; i++){
            table += row1[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row2[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row3[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row4[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row5[i];
        }
        for(int i = 0 ; i<6 ; i++){
            table += row6[i];
        }
        return table;
    }
	
	/*
	 	computersMove works in the same manner in the method "playersMove".
	 */

    public static String computersMove(int x1,int y1,int x2,int y2,String table){
        String copy = table;
        if(x1==x2){
            if(y1<y2){
                copy=table.substring(0,6*x1+y1)+table.substring(6*x1+y1+1,6*x1+y2+1)+table.charAt(6*x1+y1)+table.substring(6*(x1+1));
            }
            else if(y1>y2){
                copy=table.substring(0,6*x1)+table.charAt(6*x1+y1)+table.substring(6*x1,6*x2+y1)+table.substring(6*(x1)+y1+1);
            }
        }
        else if(y1==y2){
            if(x1<x2){
                copy = table.substring(0,6*x1+y1);
                for(int i=1 ; i<=x2-x1; i++){
                    copy +=  table.charAt(6*(x1+i)+y1)+ table.substring(6*x1+y1+1 +6*(i-1),6*(x1+i)+y1);

                }
                copy += table.charAt(6*x1+y1) + table.substring(6*(x2)+y2+1);
            }
            else if(x1>x2){
                copy=table.substring(0,y2)+table.charAt(6*x1+y1);
                for(int i=1;i<=(x1-x2);i++){
                    copy+=table.substring(6*(x2+i-1)+y2+1,6*(x2+i)+y2)+table.charAt(6*(x2+i-1)+y2);
                }
                copy+=table.substring(6*x1+y1+1);
            }
        }

        return copy;
    }
	
	/*	controller method is generated so as to control whether after the last action, there exists a winner or not.
	 	As mentioned in the project report, a row or column filled with same piece brings the win.
	 	The controller method takes 6 Arrays which indicate rows one by one and String table which is the single lined form
	 	of the current board configuration. Then, controller method first checks whether each column is filled with Xs or Os by checking
	 	the same index of arrays.
	 	If true isn't returned after the first for loop is exitted, then second for loop checks whether each row is filled with Xs or Os.
	 	In contrary of the first for loop, here we used a single lined String "table" to check whether each row is filled with Xs or Os.
	 	If true isn't returned after the second for loop is exitted as well as the first for loop, while loop keeps working because
	 	boolean controller returns false.
	 */

    public static boolean controller(String[] row1,String[] row2,String[] row3,String[] row4,String[] row5,String[] row6,String table){

        for(int i=0 ; i<6 ; i++){
            if((row1[i]+row2[i]+row3[i]+row4[i]+row5[i]+row6[i]).equals("XXXXXX")){
                return true;
            }
            else if((row1[i]+row2[i]+row3[i]+row4[i]+row5[i]+row6[i]).equals("OOOOOO")){
                return true;
            }

        }

        for(int i = 0; i<6; i++){
            if((table.substring(6*i,6*(i+1)).equals("XXXXXX"))){
                return true;
            }
            else if((table.substring(6*i,6*(i+1)).equals("OOOOOO"))){
                return true;
            }
        }
        return false;

    }
	
	/*	
	 	changeController method enables program to check whether the user or the computer
	 	entered valid coordinates to change. It checks first if the coordinates exists in the outer shell
	 	and then checks whether the piece which will be changed is blank ('B').
	 	While changeController returns false the program asks for new valid coordinates.
	 	When the user or the computer enters valid coordinates, playersChange or computersChange method runs
	 	according to who is to play this turn.
	 */

    public static boolean changeController(int x1, int y1,String table){

        return((x1==0 || x1==5 || y1==0 || y1==5) && table.charAt(6*x1+y1)=='B');
    }
	
	/*
		moveComputerController method enables program to check whether the computers move action is legal or not.
		To do so, the method first check the move action will be made in a row or column (2 possibilities).
		By using if, the program determines this.
		If x1=x2, this implies the move action will be made in the row and we should check whether the action is legal in the row.
		Now 2 new possibilities exists.
		The computer can move its piece from the beginning to the end and vice versa.
		To check both combinations, we use a nested if/else and if y1>y2 the program should check whether Xs of the coordinates are
		equal to 0 or 5 (to exist at the outer shell) and whether y2 is at the first column.
		On the other way, if y1<y2 the program should check whether Xs of the coordinates are
		equal to 0 or 5 (to exist at the outer shell) and whether y2 is at the last column.
		Otherwise it returns false which also checks whether computer has selected same coordinates (moved coordinate=target coordinate).
		If y1=y2, this implies the move action will be made in the column and we should check whether the action is legal in the column.
		Now 2 new possibilities exists.
		The computer can move its piece from the top to the bottom and vice versa.
		To check both combinations, we use a nested if/else and if x1>x2 the program should check whether Ys of the coordinates are
		equal to 0 or 5 (to exist at the outer shell) and whether x2 is at the first column.
		On the other way, if x1<x2 the program should check whether Ys of the coordinates are
		equal to 0 or 5 (to exist at the outer shell) and whether x2 is at the last column.
		Otherwise it returns false which also checks whether computer has selected same coordinates (moved coordinate=target coordinate).
	 */

    public static boolean moveComputerController(int x1, int y1 , int x2, int y2 , String table){
        if(x1==x2){
            if(y1>y2){
                return((table.charAt(6*x1+y1)=='O') && (x1==0 || x1==5) && (y2==0));
            }
            else if(y1<y2){
                return((table.charAt(6*x1+y1)=='O') && (x1==0 || x1==5) && (y2==5));
            }
            else{
                return false;
            }
        }
        else if(y1==y2){
            if(x1>x2){
                return((table.charAt(6*x1+y1)=='O') && (x2==0) && (y1==0 || y1==5));

            }
            else if(x1<x2){
                return((table.charAt(6*x1+y1)=='O') && (x2==5) && (y1==0 || y1==5));
            }
            else{
                return false;
            }
        }
        else{
            return false;
        }
    }
	
	/*	movePlayerController method works in the same manner with moveComputerController method.
	  	Only the difference is that whereas moveComputerController method checks whether the moved
	  	character is 'O' or not, movePlayerController method checks whether the moved character is
	  	'X' or not.
	*/

    public static boolean movePlayerController(int x1, int y1 , int x2, int y2 , String table){
        if(x1==x2){
            if(y1>y2){
                return((table.charAt(6*x1+y1)=='X') && (x1==0 || x1==5) && (y2==0));
            }
            else if(y1<y2){
                return((table.charAt(6*x1+y1)=='X') && (x1==0 || x1==5) && (y2==5));
            }
            else{
                return false;
            }
        }
        else if(y1==y2){
            if(x1>x2){
                return((table.charAt(6*x1+y1)=='X') && (x2==0) && (y1==0 || y1==5));

            }
            else if(x1<x2){
                return((table.charAt(6*x1+y1)=='X') && (x2==5) && (y1==0 || y1==5));
            }
            else{
                return false;
            }
        }
        else{
            return false;
        }
    }
}