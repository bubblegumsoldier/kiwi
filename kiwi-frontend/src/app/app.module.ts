import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { ImagebrowserComponent } from './imagebrowser/imagebrowser.component';
import { UsermanagerService } from './shared/usermanager/usermanager.service';
import { ImageloaderService } from './shared/imageloader/imageloader.service';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    ImagebrowserComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [
    UsermanagerService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
