package com.atguigu.team.service;
import com.atguigu.team.domain.Arichitect;
import com.atguigu.team.domain.Designer;
import com.atguigu.team.domain.Employee;
import com.atguigu.team.domain.Programmer;

/**
 * @Description Implementing transfer of members.
 */

public class TeamService {
    private  static int counter = 1; //value memberID
    private final int MAX_MEMBER = 5; //Max limit of team members
    private Programmer[] team = new Programmer[MAX_MEMBER];
    private int total; //Record the number of current members

    public TeamService(){
        super();
    }

    public Programmer[] getTeam(){
        Programmer[] team = new Programmer[total];
        for(int i=0; i< team.length; i++){
            team[i] = this.team[i];
        }
        return team;
    }

    public void addMember(Employee e) throws TeamException{
        if(total >= MAX_MEMBER){
            throw new TeamException("The team is already full.");
        }
        if(!(e instanceof Programmer)){
            throw new TeamException("This member is not a programmer.");
        }
        if(isExist(e)){
            throw new TeamException("This employee is already in the team.");
        }
        Programmer p = (Programmer)e;
        if(p.getStatus().getNAME().equals("BUSY")){
            throw new TeamException("This employee is already in another team.");
        }else if(p.getStatus().getNAME().equals("VOCATION")){
            throw new TeamException("This employee is on the vocation");
        }
        int numOfArch = 0, numOfDes = 0, numOfPro = 0;
        for(int i =0; i<total;i++){
            if(team[i] instanceof Arichitect){
                numOfArch++;
            }else if(team[i] instanceof Designer){
                numOfDes++;
            }else if(team[i] instanceof Programmer){
                numOfPro++;
            }
        }
        if(p instanceof Arichitect){
            if(numOfArch >= 1){
                throw new TeamException("There is one Architect at most");
            }else if(numOfDes >= 2){
                throw new TeamException("There are two Designer at most");
            }else if(numOfPro >= 3){
                throw new TeamException("There are three Programmer at most");
            }
        }

        //Add p into current team
        team[total++] = p;
        //set value to p
        p.setStatus(Status.BUSY);
        p.setMemberId(counter++);
    }

    public void removeMember(int id) throws TeamException{
        int i = 0;
        for(; i< total; i++){
            if(team[i].getMemberId() == id){
                team[i].setStatus(Status.FREE);
                break;
            }
        }
        if(i == total){
            throw new TeamException("I can't find designated employee, remove operation fails.");
        }

        for(int j = i+1; j<total;j++){
            team[j-1] = team[j];

        }
        team[total-1] = null;

    }

    private boolean isExist(Employee e){
        for(int i =0; i<total;i++){
            return team[i].getId() == e.getId();
        }
        return false;
    }
}
