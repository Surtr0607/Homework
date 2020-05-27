package com.atguigu.team.view;

import com.atguigu.team.domain.Employee;
import com.atguigu.team.domain.Programmer;
import com.atguigu.team.service.NameListService;
import com.atguigu.team.service.TeamException;
import com.atguigu.team.service.TeamService;

import java.sql.SQLOutput;

public class TeamView {
    private NameListService listSvc = new NameListService();
    private TeamService teamSvc = new TeamService();
    private boolean flag = true;

    public void enterMainMenu(){
        listAllEmployees();
        while(flag) {
            System.out.print("1-Team List 2-Add Team Member 3-Remove a Team Member 4-Exit Please choose(1-4): ");
            char menu = TSUtility.readMenuSelection();
            switch (menu) {
                case '1':
                    getTeam();
                    break;
                case '2':
                    addMember();
                    break;
                case '3':
                    deleteMember();
                    break;
                case '4':
                    System.out.println("Confirm whether to exit(Y/N)");
                    char isExit = TSUtility.readConfirmSelection();
                    if(isExit == 'Y'){
                        flag = false;
                    }

                    break;
            }
        }
    }

    /**
     * @Description Show information about all members.
     */
    private void listAllEmployees(){
        System.out.println("Show all members");
        System.out.println("-----------------------------Member View-------------------------------");
        Employee[] employees = listSvc.getAllEmployees();
        System.out.println("ID\t\tName\tAge\tSalary\tOccupation\tStatus\tBonus\tStock\tEquipment");
        for(int i = 0; i< employees.length; i++){
            System.out.println(employees[i]);
        }
        System.out.println("-----------------------------------------------------------------------");
    }
    private void getTeam(){
        System.out.println("View details of the team");
        System.out.println("------------------------------Team View--------------------------------");
        Programmer[] team = teamSvc.getTeam();
        if(team[0] == null){
            System.out.println("There is no member in the team.");
        }else{
            System.out.println("ID/TID\tName\tAge\tSalary\tOccupation\tStatus\tBonus\tStock\tEquipment");
            for(int i=0; i<team.length; i++){
                System.out.println(team[i].getDetailsForTeam());
            }
        }
        System.out.println("-----------------------------------------------------------------------");
    }
    private void addMember(){
        System.out.println("Add a team member");
        System.out.println("Please insert an ID: ");
        int id = TSUtility.readInt();
        try {
            Employee emp = listSvc.getEmployee(id);
            teamSvc.addMember(emp);
            System.out.println("Added successfully");
        } catch (TeamException e) {
            e.printStackTrace();
        }
        TSUtility.readReturn();

    }
    private void deleteMember(){
        System.out.println("Remove a team member");
        System.out.println("Please insert an ID: ");
        int id = TSUtility.readInt();
        System.out.println("Confirm if delete this member(Y/N): ");
        char isDelete = TSUtility.readConfirmSelection();
        if(isDelete == 'N'){
            return;
        }
        try {
            teamSvc.removeMember(id);
            System.out.println("Remove successfully");
        } catch (TeamException e) {
            e.printStackTrace();
        }
        TSUtility.readReturn();

    }
    public static void main(String[] args){
        TeamView view = new TeamView();
        view.enterMainMenu();

    }
}
