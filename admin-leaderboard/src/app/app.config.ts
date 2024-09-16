import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration } from '@angular/platform-browser';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes), provideClientHydration(), provideAnimationsAsync()]
};

export class AppConfig {
  static serverUrl: any = 'https://elsa-quiz.soumikdebnath.me';
  static isSignedIn: boolean = false;
  static signInKey: string = '__singing_with_http_req';
  static bearerToken: string = '';
}