import { Injectable } from '@angular/core';

import { Http, Headers, Response, RequestOptions } from '@angular/http';

import { environment } from '../../../../environments/environment';

import { UsermanagerService } from '../usermanager/usermanager.service';

import { Image } from '../model/Image';

import { LoggedInUser } from '../model/LoggedInUser';

import "rxjs/add/operator/map";
import { ImageWithFeedback } from "../model/ImageFeedback";

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
        this.getNextNImagesForUser(n, user).then(resolve).catch(reject);
      }).catch(reject);
    });
    return p;
  }

  private getNextNImagesForUser(n :number, user :LoggedInUser) :Promise<Image[]>
  {
    return new Promise<Image[]>((resolve, reject) => {
      let fullUrl = ImageloaderService.RECOMMENDATION_ENDPOINT + user.name + "/" + n;
      this.http.get(fullUrl).subscribe((result) => {
        let recommendation = result.json();
        this.onRecommendationResponse(recommendation).then(resolve).catch(reject);
      }, error => reject);
    });
  }

  private onRecommendationResponse(recommendation :any) :Promise<Image[]>
  {
    return new Promise<Image[]>((resolve, reject) => {
      let returnValue :Image[] = ImageloaderService.convertResultToImages(recommendation);
      console.log(returnValue);
      resolve(returnValue);
    });
  }

  private static convertResultToImages(result :any) :Image[]
  {
    return result.recommendations.posts.map(this.convertRecommendationToImage);
  }

  private static convertRecommendationToImage(recommendedPost: any): Image {
    return new Image(recommendedPost);
  }

  public sendFeedback(
    votedImage: ImageWithFeedback
  ): Promise<ImageWithFeedback> {
    return new Promise<ImageWithFeedback>((resolve, reject) => {
      this.usermanager
        .getCurrentUser()
        .then(user => {
          const request = {
            feedback: {
              user: user.name,
              post: votedImage.id,
              vote: votedImage.feedback
            }
          };

          this.sendFeedbackRequest(request)
            .then(() => resolve(votedImage))
            .catch(reject);
        })
        .catch(reject);
    });
  }

  private sendFeedbackRequest(request) :Promise<void>
  {
    return new Promise<void>((resolve, reject) => {
      let headers = new Headers({ 'Content-Type': 'application/json' });
      let options = new RequestOptions({ headers: headers });
      this.http.post(ImageloaderService.FEEDBACK_ENDPOINT, JSON.stringify(request), options).subscribe((value :Response) => {
        console.log(JSON.stringify(value));
        resolve();
      }, reject);
    });
  }
}
