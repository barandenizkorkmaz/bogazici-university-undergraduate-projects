import java.util.Scanner; //enables us to use scanner

public class main {
    public static void main(String[] args) {
        Scanner console = new Scanner(System.in); //allows us to read input
        introduction();
        String answer = "";  //String 'answer' will be filled by the next user token.
        String board = "ABGERTFFAKEMGVJA";  //String 'board' is a sequence of characters on a single line which constitutes the default configuraiton of the board.
        answer = console.next();
        if (answer.equalsIgnoreCase("No")) { //As mentioned above, String 'answer' filled with 'Yes' or 'No' by the scanner determines whether the default configuration will be used or not. If the answer is yes, program skips this 'if' part and String 'board' is still set as the default configuration. If the answer is no, 'if' method resets the String 'board' and asks each row in the following for loop, then stores it.
            board = "";
            for (int i = 1; i <= 4; i++) { //The for loop operates 4 times to ask each row into the user.
                System.out.println("Enter row " + i + " of the board:"); //'i' impies the row number.
                board += console.next(); //The new formation of board will be determined by adding each rows entered by the user into it.
            }
        }
        System.out.println("This is the board configuration now:");
        for (int i = 1; i <= 4; i++) { //The for loop enables us to divide String 'board' into 4 parts which are rows in fact.
            System.out.println(board.substring(4 * (i - 1), 4 * i)); // board.substring method makes the seperating process.
        }
        System.out.println("How many moves do you want to make?");
        int moves = console.nextInt(); //The answer of user into the question above is stored here as the int 'moves'.
        System.out.println("Make a move and press enter. After each move, the board configuration and your total points will be printed. Input the coordinates to be swapped.");
		/* The following for loop operates by using the int 'move' which marks the number of moves will be made by the user.
		   For each move for loop asks the x's and y's of the new characters which will be swapped and the new formation of board is configured by the swap method which is explained below. 
		 */
        for (int i = 1; i <= moves; i++) {
            int x1 = console.nextInt(); //The x value of 1st character.
            int y1 = console.nextInt(); //The y value of 1st character.
            int x2 = console.nextInt(); //The x value of 2nd character.
            int y2 = console.nextInt(); //The y value of 2nd character.
            if (x1 > x2) { //nested if/else method redirects my swap method in a way in which no matter the user enters the closer character or not, it reorganizes the swap method in a way that the swap method picks the closer character and swaps it with the farther one.
                board = swap(board, x1, y1, x2, y2);
            } else if (x1 < x2) {
                board = swap(board, x2, y2, x1, y1);
            } else {
                if (y1 > y2) {
                    board = swap(board, x1, y1, x2, y2);
                } else {
                    board = swap(board, x2, y2, x1, y1);
                }
            }
            System.out.println("This is the board configuration now:");
            for (int a = 1; a <= 4; a++) { //This for loop prints the rows of the current configuration of the board divided by the board.substring method.
                System.out.println(board.substring(4 * (a - 1), 4 * a)); //The String 'board' will be divided by the board.substring method.
            }
            int s=Score(board); //Score is stored as a value in the int 's' and printed in the following println command.
            System.out.println("Your total score is "+s);

        }
        System.out.println("Thank you for playing this game.");
    }

    public static void introduction() { //This method prints the introduction sentences when the user runs the code.
        System.out.println("Welcome to this weird game of SWAP");
        System.out.println("Do you want to use the default board configuration?");
    }
	
	/* The following method, Swap method, is created in a way that it finds the character by using the coordinates of character which is marked by the user and configures the board again by swapping this two characters and returns the new form of String board. 
	   This is why char m and char n characters are generated. 
	   They are connected to the xs and ys (the row number and the column number) of characters which are going to be swapped.
	   This method is used above in a way that it compares the xs and ys of entered coordinates.
	   As mentioned above, String board is declared as a single line but the problem is that we have no guarantee about whether the user will enter the closer character first.
	   So swap method is reorganized in a way that it always picks the closer character first and swaps with the farther one when using it.
	   Finally, it takes the new form of the board by using returned String board by the swap method and by the for loop, it prints the String board seperated into 4 rows which will announce the user the current configuration of the board. 
	 
	 */

    public static String swap(String board, int x1, int y1, int x2, int y2) {
        char m = board.charAt(4 * (x1 - 1) + y1 - 1);
        char n = board.charAt(4 * (x2 - 1) + y2 - 1);
        board = board.substring(0, 4 * (x2 - 1) + y2 - 1) + m + board.substring(4 * (x2 - 1) + y2, 4 * (x1 - 1) + y1 - 1) + n + board.substring(4 * (x1 - 1) + y1);
        return board;
    }

    public static int Score(String board){ //score method takes the String board as a parameter and returns int score which is the score of the user.
        int score=0; //So as to reset the score of the user in each time the program's run, it is assigned into 0.
		/*The following for loop is the part where we calculate the score of the user.
		 *The for loop simply enables us to analyze each character of the String 'board' which is a single line. 
		  The score method enables us to compare whether following characters are the same or not by CharAt method, 
		  but it distinguishes whether they are on the same row or not by using mod in if method. 
		 */

        for(int i=0;i<15;i++){ //The for loop operates from 0 which implies the initial character of the board until 'i' gets 15 because we don't need to analyze the last character of the board.
            if(board.charAt(i)==board.charAt(i+1) && (i%4)!=3){ //As mentioned above, if method enables us to compare whether following characters are the same or not by CharAt method, but it distinguishes whether they are on the same row or not by using mod in if method.Character indexes of each row are increasing from 0 to 3. Which means, if  the index value of character at i is 3, i is the last character of its row, so user cannot earn any score if the character at i+1 is the same as the one at i.
                score++; //If the conditions mentioned above are provided, score increases by 1.
            }
        }
        return score; //Eventually, it calculates the score of user in each move.
    }
}