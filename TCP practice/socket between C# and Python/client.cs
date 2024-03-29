using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class Program
{
    static void Main(string[] args)
    {
        try
        {
            // 服务器IP地址和端口号
            string serverIP = "服务器IP地址";
            int serverPort = 12345;

            // 创建一个Socket对象
            Socket clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            // 连接到服务器
            clientSocket.Connect(IPAddress.Parse(serverIP), serverPort);

            // 发送消息给服务器
            string messageToSend = "Hello, Server!";
            byte[] bytesToSend = Encoding.UTF8.GetBytes(messageToSend);
            clientSocket.Send(bytesToSend);

            // 接收来自服务器的响应
            byte[] bytesReceived = new byte[1024];
            int bytesReceivedCount = clientSocket.Receive(bytesReceived);
            string messageReceived = Encoding.UTF8.GetString(bytesReceived, 0, bytesReceivedCount);
            Console.WriteLine("收到服务器的消息：{0}", messageReceived);

            // 关闭Socket连接
            clientSocket.Shutdown(SocketShutdown.Both);
            clientSocket.Close();
        }
        catch (Exception ex)
        {
            Console.WriteLine("发生异常：{0}", ex.ToString());
        }
    }
}
