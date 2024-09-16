import { Component } from '@angular/core';
import { DashboardService } from './dashboard.service';
import { Route, Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent {
  profileName: string = 'Loading...';

  constructor(private dashboardService: DashboardService, private router: Router) {}

  ngOnInit(): void {
    this.dashboardService.getProfileInfo().subscribe({
      next: (response) => {
        if (response.status) {
          this.profileName = `${response.result[0].firstName} ${response.result[0].lastName}`;
        }
      },
      error: (error) => {
        console.error('Error fetching profile name:', error);
        this.profileName = 'Unknown User'; // Fallback text in case of error
      },
    });
  }

  onSignOut() {
    localStorage.clear();
    this.router.navigate(['/auth/sign-in']);
  }

  // Data for Pie Chart (Wrong and Right Ratio)
  public pieChartData = [
    { name: 'Right', value: 70 },
    { name: 'Wrong', value: 30 },
  ];

  // Data for Vertical Bar Chart (Wrong and Right)
  public barChartData = [
    { name: 'Right', value: 70 },
    { name: 'Wrong', value: 30 },
  ];

  // Data for Area Chart (Last 30 Days Participants)
  public lineChartData = [
    {
      name: 'Participants',
      series: [
        { name: 'Day 1', value: 150 },
        { name: 'Day 2', value: 200 },
        { name: 'Day 3', value: 180 },
        { name: 'Day 4', value: 250 },
        // Add data for 30 days here
        { name: 'Day 30', value: 300 },
      ],
    },
  ];

  // Data for Bar Chart (Top 10 Users with Marks)
  public topMarksChartData = [
    { name: 'User 1', value: 95 },
    { name: 'User 2', value: 90 },
    { name: 'User 3', value: 85 },
    { name: 'User 4', value: 80 },
    { name: 'User 5', value: 78 },
    { name: 'User 6', value: 75 },
    { name: 'User 7', value: 70 },
    { name: 'User 8', value: 68 },
    { name: 'User 9', value: 65 },
    { name: 'User 10', value: 60 },
  ];

  // Chart Options
  public showLabels: boolean = true;
  public animations: boolean = true;
}
