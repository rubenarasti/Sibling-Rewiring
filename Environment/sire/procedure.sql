DROP PROCEDURE IF EXISTS sp_createUser;

CREATE PROCEDURE sp_createUser(
    IN p_name VARCHAR(45),
    IN p_surname VARCHAR(45),
    IN p_school VARCHAR(80),
	IN p_email VARCHAR(150),
    IN p_password VARCHAR(45)
)
BEGIN
	if ( select exists (select 1 from tbl_user where user_email = p_email) ) THEN
	
		select 'Username Exists !!';
	
	ELSE
	
		insert into tbl_user
		(
			user_name,
			user_surname,
			user_school,
			user_email,
			user_password
		)
		values
		(
			p_name,
			p_surname,
            p_school,
			p_email,
			p_password
		);
	
	END IF;
END
