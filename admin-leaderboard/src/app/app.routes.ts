import { Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard'; // Import the guard

export const routes: Routes = [
  {
    path: 'pages',
    loadChildren: () =>
      import('./pages/pages.module').then((m) => m.PagesModule),
    canActivate: [AuthGuard], // Protect 'pages' route
  },
  {
    path: 'auth',
    loadChildren: () => import('./auth/auth.module').then((m) => m.AuthModule),
  },
  {
    path: '',
    pathMatch: 'full',
    canActivate: [AuthGuard], // Root route also protected
    loadChildren: () =>
      import('./pages/pages.module').then((m) => m.PagesModule), // If signed in, go to pages (dashboard)
  },
];
