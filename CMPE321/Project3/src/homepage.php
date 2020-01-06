<html>
    <body>
        <?php
            #these 5 variables are necessary in every php file.
            $servername = "localhost";
            $username = "root";
            $password = ""; 
            $dbname = "sheltermanagerdb"; 
            #creating connection.
            $conn = new mysqli($servername, $username, $password, $dbname);
            
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }else{
                session_start();
                
                #echo "<a href = 'select.php'>Go back</a>"."<br>"."<br>";
                //SHELTER MANAGER TABLE
                #$username = $_POST['Username'];
                #$sqlmain = "SELECT * FROM sheltermanager WHERE Username = '" . $_POST['Username'] . "' AND Password = '" . $_POST['Password']. "'";
                #$resultmain =  $conn->query($sqlmain);
                
                if(isset($_SESSION['username'])){
                    //session_start();
                    //$_SESSION['Username'] = $username;

                    echo "<a href = 'create_sheltermanager.php'>Create a Shelter Manager Record</a>"."<br>"."<br>";
                    $sql1 = "SELECT * FROM sheltermanager";
                    $result1 = $conn->query($sql1);
                    if ($result1->num_rows > 0) {
                    ?>
                    <tr>
                        <th>SHELTER MANAGERS</th>
                    </tr>
                    <table border = 3>
                        
                        <tr>
                            <th>Options</th>
                            <th>Username</th>
                            <th>Password</th>
                        </tr>
                    <?php
                    // output data of each row
                    while($row = $result1->fetch_assoc()) {
                        ?>
                        <tr>
                            <td>
                                <a href = "delete_sheltermanager.php?id=<?php echo $row["Username"]; ?>"><img src = "img/delete.png" alt = "Delete" /></a>
                                <a href = "update_sheltermanager.php?id=<?php echo $row["Username"]; ?>"><img src = "img/edit.png" alt = "Edit" /></a>
                            </td>
                            <td><?php echo $row["Username"]; ?></td>
                            <td><?php echo $row["Password"]; ?></td>
                        </tr>
                        <?php
                    }

                    ?>
                    </table>
                    <?php
                } else {
                    echo "No Shelter Managers."."<br>";
                }
                
                echo "<br>";
                
                //CARETAKER TABLE
                echo "<a href = 'create_caretaker.php'>Create a Caretaker Record</a>"."<br>"."<br>";
                echo "<a href = 'delete_caretaker_information.php'>Delete a Caretaker</a>"."<br>"."<br>";
                echo "<a href = 'search_animal_caretaker.php'>Search Animals of a Caretaker</a>"."<br>"."<br>";
                echo "<a href = 'rank_caretaker.php'>Rank Caretakers</a>"."<br>"."<br>";
                $sql2 = "SELECT * FROM Caretaker";
                $result2 =  $conn->query($sql2);
                
                if ($result2->num_rows > 0) {
                    ?>
                    <tr>
                        <th>CARETAKERS</th>
                    </tr>
                    <table border = 3>
                        
                        <tr>
                            <th>Options</th>
                            <th>Name</th>
                            <th>Surname</th>
                            <th>Animal</th>
                        </tr>
                    <?php
                    // output data of each row
                    while($row2 = $result2->fetch_assoc()) {
                        ?>
                        <tr>
                            <td>
                                <a href = "delete_caretaker.php?id=<?php echo $row2["Name"]; ?>&id2=<?php echo $row2["Surname"]; ?>&id3=<?php echo $row2["Animal"]; ?>"><img src = "img/delete.png" alt = "Delete" /></a>
                                <a href = "update_caretaker.php?id=<?php echo $row2["Name"]; ?>&id2=<?php echo $row2["Surname"]; ?>&id3=<?php echo $row2["Animal"]; ?>"><img src = "img/edit.png" alt = "Edit" /></a>
                            </td>
                            <td><?php echo $row2["Name"]; ?></td>
                            <td><?php echo $row2["Surname"]; ?></td>
                            <td><?php echo $row2["Animal"]; ?></td>
                        </tr>
                        <?php
                    }

                    ?>
                    </table>
                    <?php
                } else {
                    echo "No Caretakers"."<br>";
                }
                //ANIMAL TABLE
                echo "<br>";
                echo "<a href = 'create_animal.php'>Create an Animal Record</a>"."<br>"."<br>";
                echo "<a href = 'search_animal_without_sponsor.php'>Search Animals Without a Sponsor</a>"."<br>"."<br>";
                echo "<a href = 'view_animals_of_a_species.php'>View Animals of a Species</a>"."<br>"."<br>";
                $sql3 = "SELECT * FROM Animal";
                $result3 =  $conn->query($sql3);
                
                if ($result3->num_rows > 0) {
                    ?>
                    <tr>
                        <th>ANIMALS</th>
                    </tr>
                    <table border = 3>
                        
                        <tr>
                            <th>Options</th>
                            <th>Name</th>
                            <th>Age</th>
                            <th>Species</th>
                            <th>Caretaker</th>
                            <th>Sponsor</th>
                        </tr>
                    <?php
                    // output data of each row
                    while($row3 = $result3->fetch_assoc()) {
                        ?>
                        <tr>
                            <td>
                                <a href = "delete_animal.php?id=<?php echo $row3["Name"];?>"><img src = "img/delete.png" alt = "Delete" /></a>
                                <a href = "update_animal.php?id=<?php echo $row3["Name"];?>"><img src = "img/edit.png" alt = "Edit" /></a>
                            </td>
                            <td><?php echo $row3["Name"]; ?></td>
                            <td><?php echo $row3["Age"]; ?></td>
                            <td><?php echo $row3["Species"]; ?></td>
                            <td><?php echo $row3["Caretaker"]; ?></td>
                            <td><?php echo $row3["Sponsor"]; ?></td>
                        </tr>
                        <?php
                    }

                    ?>
                    </table>
                    <?php
                } else {
                    echo "No Animals";
                }
                
                //SPONSOR TABLE
                echo "<br>";
                echo "<a href = 'create_sponsor.php'>Create a Sponsor Record</a>"."<br>"."<br>";
                echo "<a href = 'delete_sponsor_information.php'>Delete a Sponsor</a>"."<br>"."<br>";
                echo "<a href = 'search_animal_sponsor.php'>Search Animals of a Sponsor</a>"."<br>"."<br>";
                $sql4 = "SELECT * FROM Sponsor";
                $result4 =  $conn->query($sql4);
                
                if ($result4->num_rows > 0) {
                    ?>
                    <tr>
                        <th>SPONSORS</th>
                    </tr>
                    <table border = 3>
                        
                        <tr>
                            <th>Options</th>
                            <th>Name</th>
                            <th>Surname</th>
                            <th>Phone</th>
                            <th>Animal</th>
                        </tr>
                    <?php
                    // output data of each row
                    while($row4 = $result4->fetch_assoc()) {
                        ?>
                        <tr>
                            <td>
                                <a href = "delete_sponsor.php?id=<?php echo $row4["Name"];?>&id2=<?php echo $row4["Surname"];?>&id3=<?php echo $row4["Animal"];?>"><img src = "img/delete.png" alt = "Delete" /></a>
                                <a href = "update_sponsor.php?id=<?php echo $row4["Name"];?>&id2=<?php echo $row4["Surname"];?>&id3=<?php echo $row4["Animal"];?>"><img src = "img/edit.png" alt = "Edit" /></a>
                            </td>
                            <td><?php echo $row4["Name"]; ?></td>
                            <td><?php echo $row4["Surname"]; ?></td>
                            <td><?php echo $row4["Phone"]; ?></td>
                            <td><?php echo $row4["Animal"]; ?></td>
                        </tr>
                        <?php
                    }

                    ?>
                    </table>
                    <?php
                } else {
                    echo "No Sponsors";
                }

                }
                else{
                    echo "Click <a href = 'login.php'>here</a> to log in"."<br>"."<br>";
                    #echo "Please enter a valid username and password!";
                }
                
            }
            $conn->close();
        
        ?>
    
    
    </body>


</html>