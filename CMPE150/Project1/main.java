public class main {
    public static void main(String[] args){
        Repetition1(12,13);
        Spaces(1);
        Repetition1(8,7);
        Spaces2(1);
        Repetition1(9,3);
        Spaces(1);
        Repetition1(5,9);
        Repetition2(1,11,1,4);
        Spaces(1);
        Repetition1(4,2);
        Repetition1(1,3);
        Repetition1(4,2);
        Repetition2(1,8,1,1);
        Repetition1(3,2);
        Spaces(1);
        Repetition1(3,1);
        Repetition1(3,1);
        Repetition1(8,1);
        Repetition2(1,6,1,1);
        Repetition1(6,2);
        Spaces(1);
        Repetition1(2,1);
        Repetition1(3,1);
        Repetition2(1,9,1,8);
        Repetition1(7,2);
        Spaces(1);
        Repetition1(1,1);
        Repetition1(3,2);
        Repetition2(1,8,1,9);
        Repetition1(8,2);
        Spaces(1);
        dollarSymbol(2);
        Repetition1(3,1);
        Repetition2(1,9,1,10);
        Repetition1(8,1);
        Spaces(1);
        dollarSymbol(1);
        Repetition1(3,2);
        Spaces2(1);
        Repetition1(7,14);
        Repetition1(7,1);
        Spaces(1);
        dollarSymbol(1);
        Repetition1(2,5);
        Repetition2(1,2,1,3);
        Repetition1(3,7);
        dashes(2);
        Spaces2(1);
        dollarSymbol(4);
        Repetition1(3,2);
        Spaces(1);
        dollarSymbol(11);
        Repetition2(1,7,1,3);
        Repetition1(8,5);
        Spaces(1);
        dollarSymbol(1);
        Repetition1(1,7);
        Repetition2(1,10,1,1);
        Repetition1(10,4);
        Spaces(1);
        dollarSymbol(1);
        Repetition1(1,7);
        Repetition2(1,10,1,1);
        Repetition1(10,4);
        Spaces(1);
        Repetition1(1,1);
        Repetition1(1,6);
        Repetition2(1,9,1,2);
        dashes(10);
        Spaces2(1);
        dollarSymbol(3);
        Spaces(1);
        Repetition1(2,1);
        Repetition1(1,2);
        Repetition1(2,2);
        Repetition2(1,8,1,1);
        Repetition1(9,2);
        Repetition1(1,2);
        Spaces(1);
        Repetition1(3,2);
        Repetition1(5,3);
        Repetition2(1,3,1,5);
        Repetition1(4,3);
        Repetition1(3,1);
        Spaces(1);
        Repetition1(4,2);
        Repetition2(1,5,1,15);
        Repetition1(3,2);
        Spaces(1);
        Repetition1(5,3);
        Repetition2(1,5,1,10);
        Repetition1(4,2);
        Spaces(1);
        Repetition1(7,4);
        Repetition2(1,2,1,9);
        Repetition1(2,3);
        Spaces(1);
        Repetition1(10,5);
        Repetition2(1,5,1,4);
        Spaces(1);
        Repetition1(14,7);
    }

    public static void dashes(int x){    //This method writes dashes without jumping line as many as x in the parameter.
        for(int a=1;a<=x;a++){			 //x is the number of dashes.
            System.out.print("_");
        }
    }

    public static void dollarSymbol(int y){    //This method writes dollarSymbols without jumping line as many as x in the parameter.
        for(int b=1;b<=y;b++){				   //y is the number of dollarSymbols.
            System.out.print("$");
        }
    }

    public static void Spaces(int z){    //This method is created in order to jump another line, so it is always used in "Spaces2(1);" form.
        for(int c=1;c<=z;c++){           //z is the number of Spaces(used to jump another line).
            System.out.println();
        }
    }

    public static void Spaces2(int z){    //This method writes spaces without jumping line as many as x in the parameter.
        for(int d=1;d<=z;d++){			  //z is the number of Spaces(without jumping line).
            System.out.print(" ");
        }
    }

    public static void Repetition1(int x,int y){    //This method combines dashes and dollarSymbol methods so as to diminish the number of lines in the code.
        dashes(x);									//x is the number of dashes.
        dollarSymbol(y);							//y is the number of dollarSymbol.
    }

    public static void Repetition2(int v,int x,int y,int z){    //This method combines spaces2,dashes,spaces2 and dollarSymbol methods so as to diminish the number of lines in the code.
        Spaces2(v);												//v is the number of Spaces(without jumping line).
        dashes(x);												//x is the number of dashes.
        Spaces2(y);												//y is the number of Spaces(without jumping line).
        dollarSymbol(z);										//z is the number of dollarSymbol.
    }
}