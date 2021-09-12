<html>
<body>
	<body>
      
      <h2>Enter Username and Password</h2> 
      <div class = "container form-signin">
         
         <?php
            $msg = '';
            $hash = password_hash("passtest", PASSWORD_BCRYPT);
            if (isset($_POST['login']) && !empty($_POST['username']) 
               && !empty($_POST['password'])) {
				
               if ($_POST['username'] == '1234123' && 
                  password_verify($_POST['password'], $hash)) {
                  
                  echo 'User is valid';
               }else {
                  $msg = 'Wrong username or password';
               }
            }
         ?>
      </div>
      
      <div class = "container">
      
         <form 
            action = "<?php echo htmlspecialchars($_SERVER['PHP_SELF']); 
            ?>" method = "post">
            <h4>
		<?php echo $msg; ?>
	    </h4>
            <input type = "text" name = "username" placeholder = "Student ID" required autofocus></br>
            <input type = "password" name = "password" placeholder = "password = passtest" required>
            <button type = "submit" name = "login">Log in</button>
         </form>
      </div> 
      
   </body>
</body>
</html>