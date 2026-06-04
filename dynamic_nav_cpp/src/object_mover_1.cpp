#include "rclcpp/rclcpp.hpp"
#include <gazebo_msgs/srv/set_entity_state.hpp>
#include <chrono>

class ObstacleMover : public rclcpp::Node{
    private:
    rclcpp::Client<gazebo_msgs::srv::SetEntityState>::SharedPtr client_;
    // same as 
    // std::shared_ptr<rclcpp::Client<gazebo_msgs::srv::SetEntityState>> client_;
    rclcpp::TimerBase::SharedPtr timer_;
    void move_obstacle(){
        std::shared_ptr<gazebo_msgs::srv::SetEntityState::Request> request = std::make_shared<gazebo_msgs::srv::SetEntityState::Request>();
        // we'll use auto request from now on to reduce words
        request->state.name = "cylinder_gy";
        request->state.reference_frame = "world";

        // to move in circle of radius r, angular velocity w
        double t = this->now().seconds();
        // the above line used the current node object's internal clock
        //double r = -2.0; // radius
        double w = 0.3; // ang Vel
        request->state.pose.position.x = -0.91;
        request->state.pose.position.y = 1.5 + 2.5 * sin(t * w);
        request->state.pose.position.z = 0.0;

        request->state.pose.orientation.w = 1.0;

        auto future = client_->async_send_request(request);
    }

    public:
        ObstacleMover() : Node("obstacle_mover"){
            client_ = this->create_client<gazebo_msgs::srv::SetEntityState>("/gazebo/set_entity_state");
            
            timer_ = this->create_wall_timer(std::chrono::milliseconds(30),
            std::bind(&ObstacleMover::move_obstacle, this)); // 30Hz
        }
    

};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<ObstacleMover>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

