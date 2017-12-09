import { Component, OnInit, Output, EventEmitter, HostListener } from '@angular/core';

import { UsermanagerService } from '../shared/usermanager/usermanager.service';
import { LoggedInUser } from '../shared/model/LoggedInUser';
import { UserInformation } from '../shared/model/UserInformation';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  private username :string = "";
  private loading :boolean = false;
  private errorMsg :string = "";

  constructor(private usermanager :UsermanagerService) { }

  ngOnInit() {
    this.startLoading();
    this.usermanager.isLoggedIn().then((loggedIn :boolean) => {
      if(!loggedIn)
      {
        console.log("Not logged in");
        this.stopLoading();
        return;
      }
      this.usermanager.getCurrentUser().then(this.doLogin.bind(this)).catch(console.log);
    }).catch(console.log);
  }

  onRegister()
  {
    let userinformation :UserInformation = new UserInformation(this.username);
    console.log("Register " + JSON.stringify(userinformation));
    this.startLoading();
    this.usermanager.tryRegister(userinformation).then(this.onLogin.bind(this)).catch(this.printErrorMessage.bind(this));
  }

  onLogin()
  {
    let userinformation :UserInformation = new UserInformation(this.username);
    this.startLoading();
    this.usermanager.tryLogin(userinformation, false).then(this.doLogin.bind(this)).catch(this.printErrorMessage.bind(this));
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

  private doLogin(user :LoggedInUser)
  {
    console.log("loggin in user");
    this.usermanager.broadcastLogin(user);
    console.log(user);
  }

  printErrorMessage(msg :string)
  {
    this.stopLoading();
    this.errorMsg = msg;
  }

  @HostListener('window:keyup', ['$event'])
  keyEvent(event: KeyboardEvent) {
    console.log(event);
    if(event.keyCode == 13)
    {
        //ENTER
        this.onLogin();
    }
  }
}
