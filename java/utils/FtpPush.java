package com.jianke.util;

import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPReply;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.SocketException;

public class FtpPush {

    /**
     * 文件上传
     * commons-net 3.6
     * @param url FTP服务器地址
     * @param port  FTP服务器端口
     * @param username FTP登录账号
     * @param password FTP登录密码
     * @param path  FTP服务器保存目录
     * @param filename 上传到FTP服务器上的文件名
     * @param input 输入流
     * @return boolean
     */
    public static boolean uploadFile(String url, int port,
                                     String username, String password,
                                     String path, String filename,
                                     InputStream input){
     boolean isSuccess = false;
     FTPClient ftp = new FTPClient();
//     ftp.setControlEncoding("GBK");
     try {
         int reply;
         ftp.connect(url, port);
         ftp.login(username, password);
         reply = ftp.getReplyCode();
         if (!FTPReply.isPositiveCompletion(reply)){
             ftp.disconnect();
             return isSuccess;
         }
         ftp.setFileType(FTPClient.BINARY_FILE_TYPE);
         ftp.enterLocalPassiveMode();
         ftp.makeDirectory(path);
         ftp.changeWorkingDirectory(path);
         isSuccess = ftp.storeFile(filename, input);
         input.close();
         ftp.logout();
     } catch (SocketException e) {
         e.printStackTrace();
     } catch (IOException e) {
         e.printStackTrace();
     } finally {
         if (ftp.isConnected()) {
             try {
                 ftp.disconnect();
             } catch (IOException e) {
                 e.printStackTrace();
             }
         }
     }
        return  isSuccess;
    }

    public static void uploadFromLocal(String url, int port,
                                       String username, String password,
                                       String path, String filename,
                                       String originFile){
        try {
            File file = new File(originFile);
            FileInputStream in = new FileInputStream(file);
            boolean flag = uploadFile(url, port, username,
                    password, path, filename, in);
            System.out.println("文件上传状态：" + flag);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        String originFile = "D:/idea_workspace/stockout-recommender/src/main/resources/intro.zip";
        String fileName = originFile.substring(originFile.lastIndexOf("/")+1);
        uploadFromLocal("111.17.240.2", 21, "xxxx", "xxxx",
                "/recomm", fileName, originFile);
    }
}
