import { Injectable } from '@angular/core';
import { Http, Headers, Response, RequestOptions } from '@angular/http';

import { environment } from '../../../environments/environment';
import { LoggedInUser } from '../model/LoggedInUser';
import { UserInformation } from '../model/UserInformation';

@Injectable()
export class UsermanagerService {


  private static API_SUFFIX :string = "users";
  private currentUser :LoggedInUser = null;

  private static LOCAL_STORAGE_USERNAME_KEY :string = "kiwi_username";

  private loginListeners :((user :LoggedInUser)=>void)[] = [];

  constructor(private http :Http)
  {

  }

  addLoginListener(listener :(user :LoggedInUser)=>void)
  {
    this.loginListeners.push(listener);
  }

  private getFullAPIPath() :string
  {
    return environment.kiwiAPIUrl + UsermanagerService.API_SUFFIX;
  }

  private getStoredUser() :Promise<LoggedInUser>
  {
    let promise :Promise<LoggedInUser> = new Promise<LoggedInUser>((resolve, reject) => {
      let storedUsername :string = localStorage.getItem(UsermanagerService.LOCAL_STORAGE_USERNAME_KEY);
      if(typeof storedUsername === typeof undefined || storedUsername.length <= 0)
      {
        reject();  
        return;
      }
      let loggedInUser :LoggedInUser = new LoggedInUser(storedUsername);
      resolve(loggedInUser);
    });
    return promise;
  }

  private storeUser(theUser :LoggedInUser) :Promise<void>
  {
    let promise :Promise<void> = new Promise<void>((resolve, reject) => {
      localStorage.setItem(UsermanagerService.LOCAL_STORAGE_USERNAME_KEY, theUser.name);
      resolve();
    });
    return promise;
  }

  getCurrentUser() :Promise<LoggedInUser>
  {
    let promise :Promise<LoggedInUser> = new Promise<LoggedInUser>((resolve, reject) => {
      if(this.currentUser != null)
      {
        resolve(this.currentUser);
      }
      this.initializeWithStoredUser().then(_ => {
        resolve(this.currentUser);
      }).catch(_ => {
        reject(); //TODO: Add error message and information
      });
    });
    return promise;
  }

  private initializeWithStoredUser() :Promise<void>
  {
    let promise :Promise<void> = new Promise<void>((resolve, reject) => {
      this.getStoredUser()
      .then(user => {
        this.currentUser = user;
        resolve();
      })
      .catch(reject);
    });
    return promise;
  }

  isLoggedIn() :Promise<boolean>
  {
    let promise :Promise<boolean> = new Promise<boolean>((resolve, reject) => {
      this.getCurrentUser().then(_=>{resolve(true)}).catch(_ => {resolve(false);});
    });
    return promise;
  }

  

  private login(userInformation :UserInformation) :Promise<LoggedInUser>
  {
    let promise :Promise<LoggedInUser> = new Promise<LoggedInUser>((resolve, reject) => {
      this.currentUser = LoggedInUser.createLoggedInUserByUserInformation(userInformation);
      this.storeUser(this.currentUser).then(_ => {
        resolve(this.currentUser);
      }).then(reject);
    });
    return promise;
  }

  //TODO: This method is too long
  tryLogin(userInformation :UserInformation, registerIfNotFound? :boolean) :Promise<LoggedInUser>
  {
    let promise :Promise<LoggedInUser> = new Promise<LoggedInUser>((resolve, reject) => {
      this.http.get(this.getFullAPIPath() + "/" + userInformation.name, {})
            .subscribe((rawResponse: Response) => {
                this.login(userInformation).then(resolve).catch(reject);
            }, error => {
                console.log("response");
                if(registerIfNotFound === true)
                {
                  this.tryRegister(userInformation).then(_ => {
                    this.tryLogin(userInformation, false).then(resolve).catch(reject);
                  }).catch(reject);
                  return;
                }
                reject("Invalid username"); //TODO error message
            });
    });
    return promise;
  }

  tryRegister(userInformation :UserInformation) :Promise<void>
  {
    let promise :Promise<void> = new Promise<void>((resolve, reject) => {
      let headers = new Headers({ 'Content-Type': 'text/plain' });
      let options = new RequestOptions({ headers: headers });
      this.http.post(this.getFullAPIPath() + "/" + userInformation.name, "", options)
            .subscribe((rawResponse :Response) => {
              resolve();
            }, error => {
              reject("Could not register... Invalid username (maybe already taken)"); //TODO message
            });
    });
    return promise;
  }

  broadcastLogin(user :LoggedInUser)
  {
    console.log(this.loginListeners.length);
    this.loginListeners.forEach(el => {el(user);});
  }
}
