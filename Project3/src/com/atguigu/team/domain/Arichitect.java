package com.atguigu.team.domain;

public class Arichitect extends Designer {
    private int stock;

    public Arichitect(int id, String name, int age, double salary, Equipment equipment, double bonus, int stock) {
        super(id, name, age, salary, equipment, bonus);
        this.stock = stock;
    }

    public int getStock() {
        return stock;
    }

    public void setStock(int stock) {
        this.stock = stock;
    }

    public String toString(){
        return getDetails() + "\tArchitect\t" + getStatus() + '\t' + getBonus() + "\t" + stock + '\t' + getEquipment().getDescription();
    }

    public String getDetailsForTeam(){
        return getMemberId() + "/" + getId() + "\t\t" + String.format("%3s",getName()) + '\t' + getAge() + '\t' + getSalary() + "\tProgrammer\t" + getStatus() + "\t\t\t\t\t" + getEquipment().getDescription();
    }
}
