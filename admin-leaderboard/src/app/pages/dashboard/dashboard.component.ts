import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { DashboardService } from './dashboard.service';
import { Route, Router } from '@angular/router';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';

export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
  { position: 1, name: 'Hydrogen', weight: 1.0079, symbol: 'H' },
  { position: 2, name: 'Helium', weight: 4.0026, symbol: 'He' },
  { position: 3, name: 'Lithium', weight: 6.941, symbol: 'Li' },
  { position: 4, name: 'Beryllium', weight: 9.0122, symbol: 'Be' },
  { position: 5, name: 'Boron', weight: 10.811, symbol: 'B' },
  { position: 6, name: 'Carbon', weight: 12.0107, symbol: 'C' },
  { position: 7, name: 'Nitrogen', weight: 14.0067, symbol: 'N' },
  { position: 8, name: 'Oxygen', weight: 15.9994, symbol: 'O' },
  { position: 9, name: 'Fluorine', weight: 18.9984, symbol: 'F' },
  { position: 10, name: 'Neon', weight: 20.1797, symbol: 'Ne' },
  { position: 11, name: 'Sodium', weight: 22.9897, symbol: 'Na' },
  { position: 12, name: 'Magnesium', weight: 24.305, symbol: 'Mg' },
  { position: 13, name: 'Aluminum', weight: 26.9815, symbol: 'Al' },
  { position: 14, name: 'Silicon', weight: 28.0855, symbol: 'Si' },
  { position: 15, name: 'Phosphorus', weight: 30.9738, symbol: 'P' },
  { position: 16, name: 'Sulfur', weight: 32.065, symbol: 'S' },
  { position: 17, name: 'Chlorine', weight: 35.453, symbol: 'Cl' },
  { position: 18, name: 'Argon', weight: 39.948, symbol: 'Ar' },
  { position: 19, name: 'Potassium', weight: 39.0983, symbol: 'K' },
  { position: 20, name: 'Calcium', weight: 40.078, symbol: 'Ca' },
];

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent implements AfterViewInit {
  profileName: string = 'Loading...';
  tableView = true;
  menu0Title = 'Graph View';
  isLoading = 1;
  errorMessage = '';

  constructor(
    private dashboardService: DashboardService,
    private router: Router
  ) {
  }

  displayedColumns: string[] = ['position', 'Id', 'fullName', 'score', 'submittedAt'];
  dataSource = new MatTableDataSource<any>(ELEMENT_DATA);

  @ViewChild(MatPaginator) paginator: MatPaginator;

  ngAfterViewInit() {
    this.dataSource = new MatTableDataSource<any>(ELEMENT_DATA);
    this.dataSource.paginator = this.paginator;
  }

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
    setTimeout(()=>{
      this.getTableData();
    }, 2000);
  }

  onSignOut() {
    localStorage.clear();
    this.router.navigate(['/auth/sign-in']);
  }

  switchView(): void {
    this.tableView = !this.tableView;
    if (this.tableView) {
      this.menu0Title = 'Graph View';
    } else {
      this.menu0Title = 'Table View';
    }
  }

  onRefresh(): void {
    this.isLoading = 1;
    setTimeout(()=>{
      this.getTableData();
    }, 2000);
  }

  getTableData(): void {
    this.isLoading = 1;
    this.dashboardService.getQuizResults().subscribe({
      next: (response) => {
        console.log(response);
        if (response.status) {
          const data = response.result;
          for (let i = 0; i < data.length; i++) {
            data[i].position = i;
            data[i].submittedAt = this.convertTimestampToDateTime(data[i].time);
          }
          this.dataSource = new MatTableDataSource<any>(data);
          this.dataSource.paginator = this.paginator;
          this.isLoading = 3;
        } else {
          this.errorMessage = response.message;
          this.isLoading = 2;
        }
      },
      error: (error) => {
        console.error('Error fetching data', error);
        this.errorMessage = 'Error fetching data';
        this.isLoading = 2;
        this.profileName = 'Unknown User'; // Fallback text in case of error
      },
    });
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

  convertTimestampToDateTime(timestampInSeconds: number): string {
    const date = new Date(timestampInSeconds * 1000); // Convert seconds to milliseconds

    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // getMonth() returns 0-based index
    const year = date.getFullYear();

    let hours = date.getHours();
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0'); // Add seconds

    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // The hour '0' should be '12'

    const formattedHours = String(hours).padStart(2, '0');

    return `${day}-${month}-${year} ${formattedHours}:${minutes}:${seconds} ${ampm}`;
  }
}
