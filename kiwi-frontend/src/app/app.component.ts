import { Component } from '@angular/core';
import { LoginComponent } from './login/login.component';
import { LoggedInUser } from './shared/model/LoggedInUser';
import { UsermanagerService } from './shared/usermanager/usermanager.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';
  currentView :number = 1;

  constructor(private usermanager :UsermanagerService) {
    this.usermanager.addLoginListener(this.onLogin.bind(this));
  }  

  ngOnInit()
  {

  }

  onLogin(loggedinUser :LoggedInUser)
  {
    this.changeView(1);
    console.log("test");
  }

  changeView(newTab :number)
  {
    this.currentView = newTab;
  }
}
