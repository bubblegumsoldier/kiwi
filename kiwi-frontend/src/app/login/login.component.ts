import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  private username :string = "";
  private loading :boolean = false;


  constructor() { }

  ngOnInit() {
    this.stopLoading();
  }

  onRegister()
  {
    console.log("Register " + this.username);
    this.startLoading();
  }

  onLogin()
  {
    console.log("Login " + this.username);
    this.startLoading();
  }

  private isLoading()
  {
    return this.loading;
  }

  private startLoading()
  {
    this.loading = true;
  }

  private stopLoading()
  {
    this.loading = false;
  }
}
