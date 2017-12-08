import { Injectable } from '@angular/core';

import { Http, Headers, Response } from '@angular/http';

import { environment } from '../../../environments/environment';

import { UsermanagerService } from '../usermanager/usermanager.service';

import { Image } from '../model/Image';

import { LoggedInUser } from '../model/LoggedInUser';

import 'rxjs/add/operator/map';

@Injectable()
export class ImageloaderService {

  public static RECOMMENDATION_ENDPOINT = environment.kiwiAPIUrl + "recommendation/";

  public static FEEDBACK_ENDPOINT = environment.kiwiAPIUrl + "feedback";

  constructor(private http :Http, private usermanager :UsermanagerService)
  {

  }

  public getNextNImages(n :number) :Promise<Image[]>
  {
    let p = new Promise<Image[]>((resolve, reject) => {
      if(n <= 0)
      {
        reject("n has to be larger than 0");
      }
      this.usermanager.getCurrentUser().then((user) => {
        this.getNextNImagesForUser(n, user).then(resolve).then(reject);
      }).catch(reject);
    });
    return p;
  }

  private getNextNImagesForUser(n :number, user :LoggedInUser) :Promise<Image[]>
  {
    return new Promise<Image[]>((resolve, reject) => {
      let fullUrl = ImageloaderService.RECOMMENDATION_ENDPOINT + user.name + "/" + n;
      this.http.get(fullUrl).map(res => {return res.json()}).subscribe((recommendation) => {
        this.onRecommendationResponse(recommendation).then(resolve).catch(reject);
      });
    });
  }

  private onRecommendationResponse(recommendation :any) :Promise<Image[]>
  {
    return new Promise<Image[]>((resolve, reject) => {
      resolve(ImageloaderService.convertResultToImages(recommendation));
    });
  }

  private static convertResultToImages(result :any) :Image[]
  {
    return result.posts.map(this.convertRecommendationToImage);
  }

  private static convertRecommendationToImage(recommendedPost :any) :Image
  {
    let i = new Image();
    i.id = recommendedPost.id;
    i.src = recommendedPost.src;
    i.title = recommendedPost.title;
    return i;
  }

  public sendFeedback(imageId :string, like :boolean) :Promise<void>
  {
    return new Promise<void>((resolve, reject) => {
      this.usermanager.getCurrentUser().then(user => {
        let feedback = {
          user: user,
          post: imageId,
          vote: like
        };
        let request = {
          feedback: feedback
        };
        this.sendFeedbackRequest(request).then(resolve).catch(reject);
      }).catch(reject);
    });
  }

  private sendFeedbackRequest(request) :Promise<void>
  {
    return new Promise<void>((resolve, reject) => {
      this.http.post(ImageloaderService.FEEDBACK_ENDPOINT, JSON.stringify(request)).subscribe((value :Response) => {
        console.log(JSON.stringify(value));
        resolve();
      });
    });
  }
}
