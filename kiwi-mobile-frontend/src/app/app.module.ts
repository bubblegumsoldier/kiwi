import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import { IonicApp, IonicErrorHandler, IonicModule } from 'ionic-angular';
import { SplashScreen } from '@ionic-native/splash-screen';
import { StatusBar } from '@ionic-native/status-bar';

import { MyApp } from './app.component';

import { LoginComponent } from './main/login/login.component';
import { ImagebrowserComponent } from './main/imagebrowser/imagebrowser.component';
import { UsermanagerService } from './main/shared/usermanager/usermanager.service';
import { ImageloaderService } from './main/shared/imageloader/imageloader.service';

import { FormsModule } from '@angular/forms';

import { HttpModule } from '@angular/http';
import { KiwiWrapperComponent } from './main/kiwi-wrapper/kiwi-wrapper.component';

import { HomePage } from '../pages/home/home';

@NgModule({
  declarations: [
    MyApp,
    HomePage,
    LoginComponent,
    ImagebrowserComponent,
    KiwiWrapperComponent
  ],
  imports: [
    BrowserModule,
    IonicModule.forRoot(MyApp),
    FormsModule,
    HttpModule
  ],
  bootstrap: [IonicApp],
  providers: [
    StatusBar,
    SplashScreen,
    UsermanagerService,
    ImageloaderService,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
  ],
  entryComponents: [
    MyApp,
    HomePage
  ]
})
export class AppModule {}
