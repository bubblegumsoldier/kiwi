import { Component, OnInit, HostListener } from "@angular/core";

import { Image } from "../shared/model/Image";
import { ImageWithFeedback } from "../shared/model/ImageFeedback";

import { ImageloaderService } from "../shared/imageloader/imageloader.service";

export enum KEY_CODE {
  UP_ARROW = 38,
  DOWN_ARROW = 40
}

@Component({
  selector: "app-imagebrowser",
  templateUrl: "./imagebrowser.component.html"
})
export class ImagebrowserComponent implements OnInit {
  private images: Image[] = [];
  private imageCache: Image[] = [];
  private votedImages: ImageWithFeedback[] = [];

  private static DEFAULT_STARTUP_IMAGE_NUMBER = 5;
  private static DEFAULT_NEW_IMAGE_LOADING_THRESHOLD = 5;
  private static DEFAULT_NEW_IMAGE_LOADING_NUMBER = 5;

  private loadingError :boolean = false;

  constructor(private imageloader: ImageloaderService) {}

  ngOnInit() {
    this.loadNextNImages(ImagebrowserComponent.DEFAULT_STARTUP_IMAGE_NUMBER);
  }

  loadNextNImages(n: number) {
    this.imageloader
      .getNextNImages(n)
      .then(this.imagesLoaded)
      .catch(this.onLoadingError.bind(this));
  }

  onLoadingError()
  {
    console.log("error...");
    this.loadingError = true;
  }

  onRetry()
  {
    this.loadingError = false;
    this.loadNextNImages(ImagebrowserComponent.DEFAULT_STARTUP_IMAGE_NUMBER);
  }

  public imagesLoaded = (images: Image[]) => {
    images.forEach(this.imageLoaded);
  };

  public imageLoaded = (image: Image) => {
    if (this.hasImageInCache(image.id)) {
      console.log(`duplicate! ${image.id}`);
      return; //duplicate entry will not be added
    }
    this.images.push(image);
    this.imageCache.push(image);
  };

  hasImageInCache(id: string) {
    return this.imageCache.find((img: Image) => img.id === id) !== undefined;
  }

  onDislike() {
    this.onFeedback("animateDown", false);
  }

  onLike() {
    this.onFeedback("animateUp", true);
  }

  onFeedback(animationDirection, feedback: boolean) {
    this.images[0][animationDirection] = true;
    console.log(this.images[0]);
    setTimeout(_ => {
      this.addFirstImageWithFeedback(feedback);
    }, 300);
  }

  addFirstImageWithFeedback(feedback: boolean) {
    const image = this.images.shift();
    this.votedImages.push({ id: image.id, feedback: feedback });
    this.setupFeedback();
  }

  setupFeedback() {
    const feedbackRequests = this.votedImages.map(imageFeedback =>
      this.imageloader.sendFeedback(imageFeedback)
    );
    let votedImagesSafetyCopy = this.votedImages.slice();

    this.votedImages = [];
    this.updateFeedback(feedbackRequests, votedImagesSafetyCopy);
  }

  updateFeedback(
    feedbackRequests: Promise<ImageWithFeedback>[],
    votedImagesSafetyCopy: ImageWithFeedback[]
  ) {
    Promise.all(feedbackRequests)
      .then(successfullRequests => {
        console.log(
          "All feedbacks were sent (" + successfullRequests.length + ")"
        );
        this.imageCache = this.imageCache.filter(
          img => !successfullRequests.some(feed => feed.id == img.id)
        );
      })
      .catch(error => {
        console.error(error);
        this.votedImages = this.votedImages.concat(votedImagesSafetyCopy);
      });

    this.updateIfNecessary();
  }

  updateIfNecessary() {
    console.log(this.images.length);
    if (
      this.images.length <=
      ImagebrowserComponent.DEFAULT_NEW_IMAGE_LOADING_THRESHOLD
    ) {
      console.log("update");
      this.loadNextNImages(
        ImagebrowserComponent.DEFAULT_NEW_IMAGE_LOADING_NUMBER
      );
    }
  }

  @HostListener("window:keyup", ["$event"])
  keyEvent(event: KeyboardEvent) {
    if (event.keyCode === KEY_CODE.UP_ARROW) {
      this.onLike();
    }

    if (event.keyCode === KEY_CODE.DOWN_ARROW) {
      this.onDislike();
    }
  }
}
