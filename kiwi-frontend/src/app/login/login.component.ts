import { Component, OnInit, Output, EventEmitter } from '@angular/core';

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
      this.usermanager.getCurrentUser().then(this.doLogin).catch(console.log);
    }).catch(console.log);
  }

  onRegister()
  {
    let userinformation :UserInformation = new UserInformation(this.username);
    console.log("Register " + userinformation);
    this.startLoading();
    this.usermanager.tryRegister(userinformation).then(this.onLogin).catch(console.log);
  }

  onLogin()
  {
    let userinformation :UserInformation = new UserInformation(this.username);
    this.startLoading();
    this.usermanager.tryLogin(userinformation, false).then(this.doLogin).catch(console.log);
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

  @Output()
  login :EventEmitter<LoggedInUser> = new EventEmitter<LoggedInUser>();

  private doLogin(user :LoggedInUser)
  {
    this.login.emit(user);
    console.log("loggin in user");
    console.log(user);
  }
}
