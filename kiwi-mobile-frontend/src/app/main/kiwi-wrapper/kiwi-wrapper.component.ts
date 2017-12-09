import { Component } from '@angular/core';
import { LoginComponent } from '../login/login.component';
import { LoggedInUser } from '../shared/model/LoggedInUser';
import { UsermanagerService } from '../shared/usermanager/usermanager.service';


@Component({
  selector: 'kiwi-wrapper',
  templateUrl: './kiwi-wrapper.component.html'
})
export class KiwiWrapperComponent {
  title = 'app';
  currentView :number = 0;

  constructor(private usermanager :UsermanagerService) {
    this.usermanager.addLoginListener(this.onLogin.bind(this));
  }  

  ngOnInit()
  {

  }

  onLogin(loggedinUser :LoggedInUser)
  {
    this.changeView(1);
  }

  changeView(newTab :number)
  {
    this.currentView = newTab;
  }
}
