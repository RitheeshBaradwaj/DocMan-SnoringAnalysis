package com.example.docman;

public class Userprofile {
    private String Email,Username;
    public Userprofile(String username){
        this.Username = username;
    }

    public Userprofile(String useremail, String username){
        this.Email = useremail;
        this.Username = username;
    }


    public Userprofile(){

    }
    public String getEmail() {
        return Email;
    }

    public void setEmail(String email) {
        Email = email;
    }

    public String getUsername() {
        return Username;
    }

    public void setUsername(String username) {
        Username = username;
    }
}
