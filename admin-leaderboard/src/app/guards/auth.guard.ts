import { Injectable } from '@angular/core';
import {
  CanActivate,
  Router,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
} from '@angular/router';
import { AppConfig } from '../app.config';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  constructor(private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    const isSignedIn = AppConfig.isSignedIn;

    if (isSignedIn) {
      // User is signed in, allow access to protected routes
      return true;
    } else {
      // User is not signed in, redirect to sign-in page
      this.router.navigate(['/auth/sign-in'], {
        queryParams: { returnUrl: state.url },
      });
      return false;
    }
  }
}
