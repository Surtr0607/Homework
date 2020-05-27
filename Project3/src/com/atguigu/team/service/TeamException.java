package com.atguigu.team.service;

/**
 *
 * @Description Create my own exceptions.
 * @author Qi Zhong
 * @version v1.0
 * @date 2020/5/27
 *
 */
public class TeamException extends Exception{
    static final long serialVersionUID = -3387516993124229948L;

    public TeamException(){
        super();
    }

    public TeamException(String exceptionmsg){
        super(exceptionmsg);
    }
}
